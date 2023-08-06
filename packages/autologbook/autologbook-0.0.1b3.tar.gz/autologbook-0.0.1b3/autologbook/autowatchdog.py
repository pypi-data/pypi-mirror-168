# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 10:33:35 2022

@author: elog-admin
"""

import logging
import math
import os
import shutil
import time
from datetime import datetime
from pathlib import Path

import watchdog.events
import watchdog.observers
from PyQt5 import QtCore
from tenacity import after_log, retry, retry_if_not_exception_type, stop_after_attempt, wait_fixed, wait_incrementing

from autologbook import autoconfig, autoerror, autotools
from autologbook.autoprotocol import HTMLObject, QuattroFEIPicture, Sample, VersaFEIPicture

Signal = QtCore.pyqtSignal
Slot = QtCore.pyqtSlot

log = logging.getLogger('__main__')


class MirroringHandler(watchdog.events.PatternMatchingEventHandler):
    """
    A Mirroring Handler subclassing the pattern matching event.

    This handler is receiving filesystem events from an observer looking at
    src_path.

    The events are treated in a way that the src_path is mirrored in dest_path.
    It is a mirroring handler and not a syncing handler. It means that if you
    change something in dest_path this will not be reflected in src_path.

    The strategy to improve the stability is the following:
        1. Each event callback (for example on_modified) is actually calling
           a process callback enclosed in a try/except block.
        2. The process callback is decorated with tenacity retry / wait and
           logging. In case that also the retry is failing the original
           exception is reraised and propagated back to the event callback
        3. The event callback exception is handling the problem.

    """

    def __init__(self, src_path, dest_path):
        """
        Build an instance of MirroringHandler.

        It calls the __init__ method of the PatternMatchingEventHandler
        with patters=('*'), ignore_directories=False and case_sensitive=False

        Parameters
        ----------
        src_path : Path-like or string
            The source path of the mirroring handler
        dest_path : Path-like or string
            The destination path of the mirroring handler

        Returns
        -------
        None.

        """
        self.src_path = Path(src_path)
        self.dest_path = Path(dest_path)
        log.info('Creating mirroring daemon with src: {} and dest: {}'.format(
            self.src_path, self.dest_path))
        # this is a reference to the observer queue. Set it to None now
        # and assign it later when available
        self.queue = None
        watchdog.events.PatternMatchingEventHandler.__init__(self,
                                                             patterns='*', ignore_directories=False,
                                                             case_sensitive=False)

    def on_created(self, event):
        """
        Handle an on_created event.

        Actually it does nothing since the real action is performed when
        the on_modified event is called.

        Parameters
        ----------
        event : watchdog.events

        Returns
        -------
        None.

        """
        if isinstance(event, watchdog.events.DirCreatedEvent):
            actual_dest_path = self.actual_dest(event.src_path)
            actual_dest_path.mkdir(parents=True, exist_ok=True)

    def on_modified(self, event):
        """
        Handle an on_modified event.

        It calls the process callback copy_file.

        It is to be verified what happens when to be modified is a directory

        Parameters
        ----------
        event : watchdog.events

        Returns
        -------
        None.

        """
        if isinstance(event, watchdog.events.DirModifiedEvent):
            return
        else:
            try:
                self.copy_file(event.src_path)
            except Exception as e:
                log.error('Error copying file %s, skipping it.' %
                          event.src_path)
                log.debug(e, exc_info=True)

    def on_deleted(self, event):
        """
        Handle an on_delete event.

        It calls the remove_resource function.

        Parameters
        ----------
        event : watchdog.events

        Returns
        -------
        None.

        """
        try:
            self.remove_resource(event.src_path)
        except Exception as e:
            log.error('Error removing file %s, skipping it.' % event.src_path)
            log.debug(e, exc_info=True)

    def on_moved(self, event):
        """
        Handle an on_moved event.

        It calls the move_resource function.

        Parameters
        ----------
        event : watchdog.events

        Returns
        -------
        None.

        """
        try:
            self.move_resource(event.src_path, event.dest_path)
        except Exception as e:
            log.error('Error moving %s to %s, skipping it.' %
                      event.src_path, event.dest_path)
            log.debug(e, exc_info=True)

    def get_extra_path(self, actual_path):
        """
        Calculate the extra path with respect to the root path.

        Parameters
        ----------
        actual_path : path
            The actual path.

        Returns
        -------
        extra_path : path
            The extra path of actual_path relative to the src_path.

        """
        path = Path(actual_path)
        try:
            extra_path = path.relative_to(self.src_path)
        except ValueError:
            log.exception(ValueError)
            extra_path = ''
        return extra_path

    def actual_dest(self, actual_src):
        """
        Calculate the resource destination.

        Parameters
        ----------
        actual_src : path
            Source path of a resource.

        Returns
        -------
        actual_dest : path
            The destination path calculated from the actual_src.

        """
        actual_src = Path(actual_src)
        return self.dest_path / self.get_extra_path(actual_src)

    @retry(reraise=True, stop=stop_after_attempt(autoconfig.AUTOLOGBOOK_MIRRORING_MAX_ATTEMPTS),
           wait=wait_fixed(autoconfig.AUTOLOGBOOK_MIRRORING_WAIT),
           after=after_log(log, logging.WARNING))
    def copy_file(self, src_path):
        """
        Copy a file.

        The source path is provided while the destination one is calculated.

        This function is decorated with retry in order to stabilize the watchdog.

        Parameters
        ----------
        src_path : path
            The source path of the resource.

        Returns
        -------
        None.

        """
        actual_dest_path = self.actual_dest(src_path)
        if Path(src_path).is_dir():
            # this case should never happen... but in case
            actual_dest_path.mkdir(parents=True, exist_ok=True)
        else:
            if not os.path.exists(actual_dest_path):
                actual_dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, actual_dest_path)
                log.info('Copying {} to {}'.format(
                    str(src_path), str(actual_dest_path)))

    @retry(reraise=True, stop=stop_after_attempt(autoconfig.AUTOLOGBOOK_MIRRORING_MAX_ATTEMPTS),
           wait=wait_fixed(autoconfig.AUTOLOGBOOK_MIRRORING_WAIT),
           after=after_log(log, logging.WARNING))
    def remove_resource(self, src_path):
        """
        Remove a file / directory.

        This function is decorated with retry to stabilize the watchdog.

        Parameters
        ----------
        src_path : path
            The source path of the resource.

        Returns
        -------
        None.

        """
        actual_dest_path = self.actual_dest(src_path)
        log.info("Removing {} from {}".format(
            actual_dest_path, self.dest_path))
        if actual_dest_path.is_file():

            actual_dest_path.unlink(missing_ok=True)
        else:

            shutil.rmtree(actual_dest_path, ignore_errors=True)

    @retry(reraise=True, stop=stop_after_attempt(autoconfig.AUTOLOGBOOK_MIRRORING_MAX_ATTEMPTS),
           wait=wait_fixed(autoconfig.AUTOLOGBOOK_MIRRORING_WAIT),
           after=after_log(log, logging.WARNING))
    def move_resource(self, src_path, dest_path):
        """
        Move a resource.

        this function is decorated with retry to stabilize the watchdog.

        Parameters
        ----------
        src_path : path
            The initial path of the resource.
        dest_path : path
            The final path of the resource.

        Returns
        -------
        None.

        """
        log.info('Moving {} to {}'.format(
            self.actual_dest(src_path), self.actual_dest(dest_path)))
        self.copy_file(dest_path)
        self.remove_resource(src_path)

    def process_all_existing(self):
        """
        Process all existing resources.

        When the watchdog is started, it is possible that the protocol directory
        wasn't empty, so it make sense to process all already existing resources.

        Returns
        -------
        None.

        """
        log.info('Mirroring all existing files')
        for file in self.src_path.glob('**/*'):
            self.copy_file(file)

    def set_queue_reference(self, queue):
        """
        Set the reference of the Observer queue.

        It is intended to offer the possibility to the user of performing some
        tasks depending on the amount of events in the queue waiting to be
        processed.

        Parameters
        ----------
        queue : Queue
            The event queue of the observer.

        Returns
        -------
        None.

        """
        self.queue = queue


class ProtocolEventHandler(watchdog.events.RegexMatchingEventHandler):
    """
    The basic subclass of the watchdog handler.

    It derives from the pattern matching event handler because we don't want
    to monitor all possible filesystem events but only the only that are
    relevant for the automatic protocol generation

    """

    def __init__(self, protocol):
        """
        Build an instance of the ProtocolEventHandler.

        It is a virtual class inheriting from the PatternMatchingEventHandler.
        Use its subclasses, for example QuattroELOGProtocolEventHandler

        From the protocol it gets the patterns of interest and the excluded ones
        as well and calls the constructor of the PatternMatchingEventHandler with
        these parameters
        Parameters
        ----------
        protocol : ELOGProtocol
            The instance of the protocol.

        Returns
        -------
        None.

        """
        self.protocol_instance = protocol
        self.matching_patterns, self.excluded_patterns = autotools.get_patterns_from_config()

        # this is a reference to the observer queue. Set it to None now
        # and assign it later when available
        self.queue = None

        # the dictionary of all type guessers
        # it contains pairs of ElementTypeGuessers with their ElementType
        self.type_guessers = {}

        image_file_matching = autoconfig.IMAGEFILE_MATCHING_PATTERNS
        image_file_exclude = autoconfig.IMAGEFILE_EXCLUDE_PATTERNS

        self.type_guessers[str(autotools.ElementType.MICROSCOPE_PIC)] = \
            (autotools.ElementTypeGuesser(image_file_matching, image_file_exclude),
             autotools.ElementType.MICROSCOPE_PIC)

        attachment_include_pattern = autoconfig.ATTACHMENT_MATCHING_PATTERNS
        attachment_exclude_pattern = autoconfig.ATTACHMENT_EXCLUDE_PATTERNS

        self.type_guessers[str(autotools.ElementType.ATTACHMENT_FILE)] = \
            (autotools.ElementTypeGuesser(attachment_include_pattern, attachment_exclude_pattern),
             autotools.ElementType.ATTACHMENT_FILE)

        yaml_file_include_pattern = autoconfig.YAMLFILE_MATCHING_PATTERNS
        yaml_file_exclude_pattern = autoconfig.YAMLFILE_EXCLUDE_PATTERNS

        self.type_guessers[str(autotools.ElementType.YAML_FILE)] = \
            (autotools.ElementTypeGuesser(yaml_file_include_pattern, yaml_file_exclude_pattern),
             autotools.ElementType.YAML_FILE)

        # this parameter contains a timestamp referring to the time when the
        # elog was updated.
        self.last_update = datetime.now()

        watchdog.events.RegexMatchingEventHandler.__init__(self, regexes=self.matching_patterns,
                                                           ignore_directories=True, case_sensitive=False,
                                                           ignore_regexes=self.excluded_patterns)

    def guess_element_type(self, path):
        """
        Guess the type pf element.

        Starting from the full path retrieved from the FS event, all available
        ElementTypeGuessers are checked. As soon as one is returning a valid element
        the corresponding element type is returned.

        Parameters
        ----------
        path : str, Path
            The path of the FS event.

        Returns
        -------
        etype : autotools.ElementType
            The ElementType as guessed by the given path.

        """
        for (guesser, etype) in self.type_guessers.values():
            if guesser.is_ok(path):
                return etype

    @staticmethod
    def wait_until_copy_finished(event):
        """
        Wait until the copy of the file in the event is finished.

        This method is monitoring the size of the newly added file. If it keeps
        on changing it means that is still being copied.

        The size of the file is polled with an adaptive delay. Very fast at the
        beginning and more slowly later on. The maximum polling delay is 1 sec.
        Normally only 1 interaction is necessary for a standard size TIFF file
        corresponding to a delay of 0.06s.

        Parameters
        ----------
        event : filesystem event
            This is the file system event generated by the file being
            copied.

        Returns
        -------
        None.

        """
        if isinstance(event, watchdog.events.FileCreatedEvent):
            old_size = -1
            i = 0.
            while old_size != Path(event.src_path).stat().st_size:
                old_size = Path(event.src_path).stat().st_size
                delay = 2 / math.pi * math.atan(i / 6 + 0.1)
                i += 1
                time.sleep(delay)

    def get_full_sample_name(self, new_pic_path):
        r"""
        Get the sample full name from the picture path.

        For example, if a protocol is based in:
            R:\Results\2022\1234-project-resp\
        and a picture is created with the following path:
            R:\Results\2022\1234-project-resp\Sample1\Sample1.2\Sample1.2.1\image.tif

        then the sample full name will be:
            Sample1/Sample1.2/Sample1.2.1

        Parameters
        ----------
        new_pic_path : str | Path
            The full path of the newly added picture.

        Returns
        -------
        sample_full_name: str
            The sample full name

        """
        if not isinstance(new_pic_path, Path):
            new_pic_path = Path(new_pic_path)

        return str(new_pic_path.relative_to(self.protocol_instance.path).parent).replace('\\', '/')

    def check_and_add_parents(self, new_pic_path):
        """
        Check if the parent samples of the new pictures are all existing.

        From the path of the new pictures, the list of all sample parents is
        calculated and the protocol is checked to verify that they are all there.
        If not, they are added.

        Parameters
        ----------
        new_pic_path : string or path
            The path of the newly added picture.

        Returns
        -------
        None.

        """
        if not isinstance(new_pic_path, Path):
            new_pic_path = Path(new_pic_path)

        # we need to add samples using their full_name
        # the parent lists returns something like:
        #
        #      ['SampleA', 'SampleA/SubSampleB', 'SampleA/SubSampleB/SubSampleC']
        for sample_full_name in autotools.parents_list(new_pic_path, self.protocol_instance.path):
            if sample_full_name not in self.protocol_instance.samples:
                self.protocol_instance.add_sample(Sample(sample_full_name))

    def check_and_remove_parents(self, removed_pic_path):
        """
        Check if the parents are not needed anymore and remove them.

        From the path of the newly removed picture check if the parents samples
        are still needed. If they are emtpy, they are removed.

        Parameters
        ----------
        removed_pic_path : string or path
            The path of the newly removed picture.

        Returns
        -------
        None.

        """
        if not isinstance(removed_pic_path, Path):
            removed_pic_path = Path(removed_pic_path)

        # we need to remove samples using their full_name
        # the parent lists returns something like:
        #
        #      ['SampleA', 'SampleA/SubSampleB', 'SampleA/SubSampleB/SubSampleC']
        for sample_full_name in reversed(autotools.parents_list(removed_pic_path, self.protocol_instance.path)):
            if self.protocol_instance.samples[sample_full_name].is_empty():
                log.debug('Sample %s is empty. Remove it' % sample_full_name)
                self.protocol_instance.remove_sample(sample_full_name)
            else:
                log.debug('Sample %s is not empty. Leave it' %
                          sample_full_name)
                break

    def on_created(self, event):
        """
        Handle an on_created event.

        Parameters
        ----------
        event : watchdog.event

        Returns
        -------
        None.

        """
        try:
            self.process_on_created(event)
        except FileNotFoundError as e:
            log.debug(e, exc_info=True)
            log.error(
                'File %s not found. Was it already deleted? Skipping it.' % event.src_path)

    def on_modified(self, event):
        """Handle an on_modified event."""
        try:
            self.process_on_modified(event)
        except FileNotFoundError as e:
            log.error(
                'File %s not found. Was it already deleted? Skipping it.' % event.src_path)
            log.debug(e, exc_info=True)

    def on_moved(self, event):
        """Handle an on_moved event."""
        if not event.is_directory:
            log.info('Moved event detected!')
            myevent = watchdog.events.FileDeletedEvent(event.src_path)
            try:
                self.process_on_deleted(myevent, skip_elog_update=True)
            except FileNotFoundError as e:
                log.error(
                    'File %s not found. Was it already deleted? Skipping it.' % event.src_path)
                log.debug(e, exc_info=True)
            myevent = watchdog.events.FileCreatedEvent(event.dest_path)
            try:
                self.process_on_created(myevent, skip_elog_update=False)
            except FileNotFoundError as e:
                log.error(
                    'File %s not found. Was it already deleted? Skipping it.' % event.src_path)
                log.debug(e, exc_info=True)

    def on_deleted(self, event):
        """Handle an on_deleted event."""
        try:
            self.process_on_deleted(event)
        except FileNotFoundError as e:
            log.error(
                'File %s not found. Was it already deleted? Skipping it.' % event.src_path)
            log.exception(e, exc_info=True)
        except KeyError as e:
            log.error('Can\'t find %s among the sample images. The output protocol must be verified'
                      % event.src_path)
            log.exception(e, exc_info=True)
        except Exception as e:
            log.exception(e, exc_info=True)

    def process_on_created(self, event, skip_elog_update=False):
        """
        Process the creation of a new element.

        This function is decorated with retry to improve the application stability.

        Parameters
        ----------
        event : watchdog.event

        skip_elog_update : bool, optional
            Allows to skip the posting of HTML code.
            The default is False.

        Returns
        -------
        None.

        """
        pass

    def process_on_deleted(self, event, skip_elog_update=False):
        """
        Process the deletion of a resource.

        This function is decorated with retry to improve the application stability.

        Parameters
        ----------
        event : watchdog.events

        skip_elog_update : bool, optional
            Allows to skip the posting of HTML code.
            The default is False.

        Returns
        -------
        None.

        """
        pass

    def process_on_modified(self, event, skip_elog_update=False):
        """
        Process the modification of a resource.

        This function is decorated with retry to improve the application stability.

        Parameters
        ----------
        event : watchdog.events

        skip_elog_update : bool, optional
            Allows to skip the posting of HTML code.
            The default is False.

        Returns
        -------
        None.

        """
        pass

    def set_queue_reference(self, queue):
        """
        Set the reference of the Observer queue.

        It is intended to offer the possibility to the user of performing some
        tasks depending on the amount of events in the queue waiting to be
        processed.

        Parameters
        ----------
        queue : Queue
            The event queue of the observer.

        Returns
        -------
        None.

        """
        self.queue = queue

    def update_logbook(self, skip_attachments=True):
        """
        Update the logbook entry.

        Generate the HTML code of the whole protocol and post it to the
        server.

        Parameters
        ----------
        skip_attachments : bool, optional
            Allows to skip the attachments in order to reduce the network trafic.
            The default is True.

        Returns
        -------
        None.

        """
        HTMLObject.reset_html_content()
        self.protocol_instance.generate_html()
        self.protocol_instance.post_elog_message(skip_attachments)
        self.last_update = datetime.now()

    def process_already_existing_items(self):
        """
        Process all existing items.

        This function is processing all existing items found in the protocol
        folder when the watchdog is started.

        Returns
        -------
        None.

        """

        log.info('Processing existing files in folder %s' % self.protocol_instance.path)

        for filename in sorted(autotools.reglob(path=os.path.join(self.protocol_instance.path, '**', '*'),
                                                matching_regexes=self.matching_patterns,
                                                ignore_regexes=self.excluded_patterns,
                                                recursive=True)):
            log.debug('Preprocess file %s' % filename)
            event = watchdog.events.FileCreatedEvent(
                os.path.join(filename))
            # we are using the process_on_created even if
            # the files are already existing.
            self.process_on_created(event, skip_elog_update=True)
        self.update_logbook(skip_attachments=True)


class QuattroELOGProtocolEventHandler(ProtocolEventHandler):
    """
    The QuattroELOGProtocolEventHandler.

    This is a subclass of the general ProtocolEventHandler customized for the
    Quattro microscope.

    """

    def __init__(self, protocol):
        super().__init__(protocol)

        # take the matching and exclude get_patterns from the autoconfig.
        navigation_include_pattern = autoconfig.NAVIGATION_MATCHING_PATTERNS
        navigation_exclude_pattern = autoconfig.NAVIGATION_EXCLUDE_PATTERNS

        self.type_guessers[str(autotools.ElementType.NAVIGATION_PIC)] = \
            (autotools.ElementTypeGuesser(navigation_include_pattern, navigation_exclude_pattern),
             autotools.ElementType.NAVIGATION_PIC)

    @retry(retry=retry_if_not_exception_type(autoerror.ReadOnlyEntry),
           reraise=True, stop=stop_after_attempt(autoconfig.AUTOLOGBOOK_WATCHDOG_MAX_ATTEMPTS),
           wait=wait_incrementing(autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_INCREMENT,
                                  autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MIN,
                                  autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MAX),
           after=after_log(log, logging.WARNING))
    def process_on_created(self, event, skip_elog_update=False):
        """
        Process the creation of a new element.

        This function is decorated with retry to improve the application stability.

        Parameters
        ----------
        event : watchdog.event

        skip_elog_update : bool, optional
            Allows to skip the posting of HTML code.
            The default is False.

        Returns
        -------
        None.

        """
        # wait until the copy process is finished.
        # it shouldn't take too long
        self.wait_until_copy_finished(event)

        # guess the element type
        etype = self.guess_element_type(event.src_path)

        logbook_changed = False
        # first we need to know what has been added
        if etype == autotools.ElementType.NAVIGATION_PIC:
            self.protocol_instance.add_navigation_camera_image(event.src_path)
            logbook_changed = True

        elif etype == autotools.ElementType.ATTACHMENT_FILE:
            self.protocol_instance.add_attachment(event.src_path)
            logbook_changed = True

        elif etype == autotools.ElementType.YAML_FILE:
            self.protocol_instance.initialize_yaml()
            logbook_changed = True

        elif etype == autotools.ElementType.MICROSCOPE_PIC:
            # we have a new image and we need to check if its sample and samples
            # parents already exists
            self.check_and_add_parents(event.src_path)

            # we know that sample_name already exists because it is checked
            # in the check_and_add_parents
            sample_full_name = self.get_full_sample_name(event.src_path)
            if sample_full_name:
                logbook_changed = True
                self.protocol_instance.samples[sample_full_name].add_microscope_picture(
                    QuattroFEIPicture(event.src_path))
            else:
                # if we get here, it is because the user saved a tif file in the protocol
                # base folder and we don't know what to do with this. Just ignore it.
                log.debug(
                    'Found a TIFF file in the protocol base folder. Doing nothing')

        # it is the moment to update the elog. This will be done if based on the following conditions
        #   A = the logbookChanged is True, otherwise it make no sense
        #   B = the skip_elog_update is False, it the user doesn't want we don't do it
        #   C = the observer is empty
        #   D = last update > max Delta Time
        #
        #   (A and B) and (C or D)
        a = logbook_changed
        b = not skip_elog_update
        c = self.queue.empty()
        dt = datetime.now().timestamp() - self.last_update.timestamp()
        d = dt > autoconfig.AUTOLOGBOOK_WATCHDOG_MIN_DELAY
        # if logbookChanged and not skip_elog_update:
        if (a and b) and (c or d):
            self.update_logbook(skip_attachments=True)
        else:
            if a:
                log.info('Skipping ELOG updates')
            log.debug('Reason why skipping (Not requested: %s - Empty Queue: %s - DeltaT = %.1f s)'
                      % (a and b, c, dt))

    @retry(retry=retry_if_not_exception_type(autoerror.ReadOnlyEntry),
           reraise=True, stop=stop_after_attempt(autoconfig.AUTOLOGBOOK_WATCHDOG_MAX_ATTEMPTS),
           wait=wait_incrementing(autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_INCREMENT,
                                  autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MIN,
                                  autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MAX),
           after=after_log(log, logging.WARNING))
    def process_on_deleted(self, event, skip_elog_update=False):
        """
        Process the deletion of a resource.

        This function is decorated with retry to improve the application stability.

        Parameters
        ----------
        event : watchdog.events

        skip_elog_update : bool, optional
            Allows to skip the posting of HTML code.
            The default is False.

        Returns
        -------
        None.

        """
        etype = self.guess_element_type(event.src_path)

        logbook_changed = False
        # first we need to know what has been deleted
        if etype == autotools.ElementType.NAVIGATION_PIC:
            self.protocol_instance.remove_navigation_camera_image(event.src_path)
            self.protocol_instance.remove_from_yaml(event.src_path)
            logbook_changed = True

        elif etype == autotools.ElementType.ATTACHMENT_FILE:
            self.protocol_instance.remove_attachment(event.src_path)
            self.protocol_instance.remove_from_yaml(event.src_path)
            logbook_changed = True

        elif etype == autotools.ElementType.YAML_FILE:
            self.protocol_instance.initialize_yaml()
            logbook_changed = True

        elif etype == autotools.ElementType.MICROSCOPE_PIC:
            # we got an imaged removed.

            sample_full_name = self.get_full_sample_name(event.src_path)
            if sample_full_name:
                # the tif image is in a sample folder

                # first we remove the yaml section if existing.
                # the picture id is used as a key for that dictionary.
                pic_id = self.protocol_instance.samples[sample_full_name].images[event.src_path].getID(
                )
                self.protocol_instance.remove_from_yaml(pic_id)

                # now remove the picture from the sample
                self.protocol_instance.samples[sample_full_name].remove_microscope_picture_path(
                    event.src_path)
                logbook_changed = True
                log.debug('Removing image (%s) from an existing sample (%s)' % (
                    event.src_path, sample_full_name))
                self.check_and_remove_parents(event.src_path)

            else:
                # the tif image is in the protocol folder.
                # we just ignore it.
                log.debug(
                    'Found a TIFF file in the protocol base folder. Doing nothing')

        # it is the moment to update the elog. This will be done if based on the following conditions
        #   A = the logbookChanged is True, otherwise it make no sense
        #   B = the skip_elog_update is False, it the user doesn't want we don't do it
        #   C = the observer is empty
        #   D = last update > max Delta Time
        #
        #   For some obscure reason the queue is always empty when deleting.
        #   I'm changing the condition to take into account just the delay.
        #
        #   (A and B) and (D)
        a = logbook_changed
        b = not skip_elog_update
        c = self.queue.empty()
        dt = datetime.now().timestamp() - self.last_update.timestamp()
        d = dt > autoconfig.AUTOLOGBOOK_WATCHDOG_MIN_DELAY
        log.debug('Posting? (Not requested: %s AND (Empty Queue: %s (%s) OR DeltaT = %s (%.1f s)) -> %s' %
                  (a and b, c, self.queue.qsize(), d, dt, (a and b) and d))
        # if logbookChanged and not skip_elog_update:
        if (a and b) and d:
            self.update_logbook(skip_attachments=True)
        else:
            log.info('Skipping ELOG updates')
            log.debug('Reason why skipping (Not requested: %s - Empty Queue: %s - DeltaT = %.1f s)'
                      % (a and b, c, dt))

    @retry(retry=retry_if_not_exception_type(autoerror.ReadOnlyEntry),
           reraise=True, stop=stop_after_attempt(autoconfig.AUTOLOGBOOK_WATCHDOG_MAX_ATTEMPTS),
           wait=wait_incrementing(autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_INCREMENT,
                                  autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MIN,
                                  autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MAX),
           after=after_log(log, logging.WARNING))
    def process_on_modified(self, event, skip_elog_update=False):
        """
        Process the modification of a resource.

        This function is decorated with retry to improve the application stability.

        Parameters
        ----------
        event : watchdog.events

        skip_elog_update : bool, optional
            Allows to skip the posting of HTML code.
            The default is False.

        Returns
        -------
        None.

        """
        # guess the element type
        etype = self.guess_element_type(event.src_path)

        logbook_changed = False
        if etype == autotools.ElementType.YAML_FILE:
            # there is a new yaml file.
            self.protocol_instance.initialize_yaml()
            logbook_changed = True

        if logbook_changed and not skip_elog_update:
            self.update_logbook(skip_attachments=True)


class VersaELOGProtocolEventHandler(ProtocolEventHandler):
    """
    The VersaELOGProtocolEventHandler.

    This is a subclass of the general ProtocolEventHandler customized for the
    Versa microscope.

    """

    def __init__(self, protocol):
        super().__init__(protocol)

    @retry(retry=retry_if_not_exception_type(autoerror.ReadOnlyEntry),
           reraise=True, stop=stop_after_attempt(autoconfig.AUTOLOGBOOK_WATCHDOG_MAX_ATTEMPTS),
           wait=wait_incrementing(autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_INCREMENT,
                                  autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MIN,
                                  autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MAX),
           after=after_log(log, logging.WARNING))
    def process_on_created(self, event, skip_elog_update=False):
        """
        Process the creation of a new element.

        This function is decorated with retry to improve the application stability.

        Parameters
        ----------
        event : watchdog.event

        skip_elog_update : bool, optional
            Allows to skip the posting of HTML code.
            The default is False.

        Returns
        -------
        None.

        """
        # wait until the copy process is finished.
        # it shouldn't take too long
        self.wait_until_copy_finished(event)

        # guess the element type
        etype = self.guess_element_type(event.src_path)

        logbook_changed = False
        # first we need to know what has been added
        if etype == autotools.ElementType.ATTACHMENT_FILE:
            self.protocol_instance.add_attachment(event.src_path)
            logbook_changed = True

        elif etype == autotools.ElementType.YAML_FILE:
            self.protocol_instance.initialize_yaml()
            logbook_changed = True

        elif etype == autotools.ElementType.MICROSCOPE_PIC:
            # we have a new image and we need to check if its sample and samples
            # parents already exists
            self.check_and_add_parents(event.src_path)

            # we know that sample_name already exists because it is checked
            # in the check_and_add_parents
            sample_full_name = self.get_full_sample_name(event.src_path)
            if sample_full_name:
                logbook_changed = True
                self.protocol_instance.samples[sample_full_name].add_microscope_picture(
                    VersaFEIPicture(event.src_path))
            else:
                # if we get here, it is because the user saved a tif file in the protocol
                # base folder and we don't know what to do with this. Just ignore it.
                log.debug(
                    'Found a TIFF file in the protocol base folder. Doing nothing')

        # it is the moment to update the elog. This will be done if based on the following conditions
        #   A = the logbookChanged is True, otherwise it make no sense
        #   B = the skip_elog_update is False, it the user doesn't want we don't do it
        #   C = the observer is empty
        #   D = last update > max Delta Time
        #
        #   (A and B) and (C or D)
        a = logbook_changed
        b = not skip_elog_update
        c = self.queue.empty()
        dt = datetime.now().timestamp() - self.last_update.timestamp()
        d = dt > autoconfig.AUTOLOGBOOK_WATCHDOG_MIN_DELAY
        log.debug('Posting? (Not requested: %s AND (Empty Queue: %s (%s) OR DeltaT = %s (%.1f s)) -> %s' %
                  (a and b, c, self.queue.qsize(), d, dt, (a and b) and (c or d)))
        # if logbookChanged and not skip_elog_update:
        if (a and b) and (c or d):
            self.update_logbook(skip_attachments=True)
        else:
            if a:
                log.info('Skipping ELOG updates')
            log.debug('Reason why skipping (Not requested: %s - Empty Queue: %s - DeltaT = %.1f s)'
                      % (a and b, c, dt))

    @retry(retry=retry_if_not_exception_type(autoerror.ReadOnlyEntry),
           reraise=True, stop=stop_after_attempt(autoconfig.AUTOLOGBOOK_WATCHDOG_MAX_ATTEMPTS),
           wait=wait_incrementing(autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_INCREMENT,
                                  autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MIN,
                                  autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MAX),
           after=after_log(log, logging.WARNING))
    def process_on_deleted(self, event, skip_elog_update=False):
        """
        Process the deletion of a resource.

        This function is decorated with retry to improve the application stability.

        Parameters
        ----------
        event : watchdog.events

        skip_elog_update : bool, optional
            Allows to skip the posting of HTML code.
            The default is False.

        Returns
        -------
        None.

        """
        etype = self.guess_element_type(event.src_path)

        logbook_changed = False
        # first we need to know what has been added
        if etype == autotools.ElementType.ATTACHMENT_FILE:
            self.protocol_instance.remove_attachment(event.src_path)
            self.protocol_instance.remove_from_yaml(event.src_path)
            logbook_changed = True

        elif etype == autotools.ElementType.MICROSCOPE_PIC:
            # we got an imaged removed.
            sample_full_name = self.get_full_sample_name(event.src_path)
            if sample_full_name:
                # the tif image is in a sample folder

                # first we remove the yaml section if existing.
                # the picture id is used as a key for that dictionary.
                pic_id = self.protocol_instance.samples[sample_full_name].images[event.src_path].getID(
                )
                self.protocol_instance.remove_from_yaml(pic_id)

                # now remove the picture from the sample
                self.protocol_instance.samples[sample_full_name].remove_microscope_picture_path(
                    event.src_path)
                logbook_changed = True
                log.debug('Removing image (%s) from an existing sample (%s)' % (
                    event.src_path, sample_full_name))
                self.check_and_remove_parents(event.src_path)

            else:
                # the tif image is in the protocol folder.
                # we just ignore it.
                log.debug(
                    'Found a TIFF file in the protocol base folder. Doing nothing')

        elif etype == autotools.ElementType.YAML_FILE:
            # there is a new yaml file.
            self.protocol_instance.initialize_yaml()
            logbook_changed = True

        # it is the moment to update the elog. This will be done if based on the following conditions
        #   A = the logbookChanged is True, otherwise it make no sense
        #   B = the skip_elog_update is False, it the user doesn't want we don't do it
        #   C = the observer is empty
        #   D = last update > max Delta Time
        #
        #   For some obscure reason the queue is always empty when deleting.
        #   I'm changing the condition to take into account just the delay.
        #
        #   (A and B) and (D)
        a = logbook_changed
        b = not skip_elog_update
        c = self.queue.empty()
        dt = datetime.now().timestamp() - self.last_update.timestamp()
        d = dt > autoconfig.AUTOLOGBOOK_WATCHDOG_MIN_DELAY
        log.debug('Posting? (Not requested: %s AND (Empty Queue: %s (%s) OR DeltaT = %s (%.1f s)) -> %s' %
                  (a and b, c, self.queue.qsize(), d, dt, (a and b) and d))
        # if logbookChanged and not skip_elog_update:
        if (a and b) and d:
            self.update_logbook(skip_attachments=True)
        else:
            log.info('Skipping ELOG updates')
            log.debug('Reason why skipping (Not requested: %s - Empty Queue: %s - DeltaT = %.1f s)'
                      % (a and b, c, dt))

    @retry(retry=retry_if_not_exception_type(autoerror.ReadOnlyEntry),
           reraise=True, stop=stop_after_attempt(autoconfig.AUTOLOGBOOK_WATCHDOG_MAX_ATTEMPTS),
           wait=wait_incrementing(autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_INCREMENT,
                                  autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MIN,
                                  autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MAX),
           after=after_log(log, logging.WARNING))
    def process_on_modified(self, event, skip_elog_update=False):
        """
        Process the modification of a resource.

        This function is decorated with retry to improve the application stability.

        Parameters
        ----------
        event : watchdog.events

        skip_elog_update : bool, optional
            Allows to skip the posting of HTML code.
            The default is False.

        Returns
        -------
        None.

        """
        # guess the element type
        etype = self.guess_element_type(event.src_path)

        logbook_changed = False
        if etype == autotools.ElementType.YAML_FILE:
            # there is a new yaml file.
            self.protocol_instance.initialize_yaml()
            logbook_changed = True

        if logbook_changed and not skip_elog_update:
            self.update_logbook(skip_attachments=True)
