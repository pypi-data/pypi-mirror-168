"""String"""

import os
import re
import copy
import difflib

import ass


class InputCountException(Exception):
    """ Exception raised when the number of available files in the directory
        of one input file does not match with the number of availabile files
        of the other input files. Also used for attachments, chapters, etc.

    Attributes:
        file_count (int): number of files found in directory
        expected_file_count (int): expected number of files to be found in directory
    """

    def __init__(self, file_count: int, expected_file_count: int,
                 message: str = "Number of input files does not correspond to each other"):
        self.file_count = file_count
        self.expected_file_count = expected_file_count
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Got {self.file_count} instead of {self.expected_file_count} -> {self.message}"


def similar(match1: str, match2: str) -> float:
    """ Generate similarity ratio of two strings """
    return difflib.SequenceMatcher(None, match1, match2).ratio()


def delete_indices_from_list(indices: set, data_list: list) -> list:
    """ Deletes values from a list at a given set of indices """
    for indice in sorted(indices, reverse=True):
        # Reverse sort so the loop won't mess up as we delete the indices.
        del data_list[indice]


def move_indices_list_to_list(indices: set, receiving_list: list, providing_list: list):
    """ Moves values from providing_list to receiving_list at the given indices """
    for indice in sorted(indices, reverse=True):
        receiving_list.append(providing_list[indice])
        del providing_list[indice]


class DialogueMerger:
    """ Merges two subtitles, using one subtitle file as the base and another for the dialogue """

    def __init__(self, export_dialogue_changes: bool = True):
        self.export_dialogue_changes = export_dialogue_changes

    def __sort_subtitle_events(self, events: list):
        return sorted(events, key=lambda e: e.start)

    def __keep_dialogue(self, subtitle_events: list) -> list:
        """ Retrieves all dialogue events from subtitle events """
        return [event for event in subtitle_events
                if re.match("^Default|^Alt", event.style) and event.text
                and not event.dump_with_type().startswith("Comment: ")]

    def __remove_dialogue(self, subtitle_events: list) -> list:
        """ Retrieves all non-dialogue events from subtitle events """
        return [event for event in subtitle_events
                if not re.match("^Default|^Alt", event.style) or not event.text
                or event.dump_with_type().startswith("Comment: ")]

    def __find_events_misalignments(self, base_sub, dialogue_sub) -> tuple[set]:
        """ Detect which lines need to be deleted from the base_subtitle
            dialogue events and which dialogue events from the dialogue_subtitle
            must be copied over to the base_subtitle. Both input subtitles must
            already be filtered to only contain the dialogue events.
        """
        offset = 0  # Index offset on the dialogue_subtitle iterations
        delete_indices = set()
        copy_indices = set()

        for index, base_event in enumerate(base_sub.events):
            remaining_lines = len(base_sub.events) - index
            lookahead = 8 if remaining_lines > 8 else remaining_lines - 1
            dialogue_event = dialogue_sub.events[index+offset]
            event_similarity = similar(base_event.text, dialogue_event.text)

            if event_similarity < 0.6:
                comparison_problem = True

                total_similarity = 0
                for iteration in range(lookahead):
                    # We check some of the continuing comparisons to prevent false positives. If we
                    # have a problem then the rest will be misaligned and all have low similarity
                    # We use the average since multiple modifications in a row may otherwise
                    # influence the results
                    total_similarity += similar(base_sub.events[index+iteration].text,
                                                dialogue_sub.events[index+offset+iteration].text)
                    if (total_similarity / lookahead) > 0.6:
                        comparison_problem = False

                if comparison_problem:
                    for iteration in range(lookahead):
                        copy_similarity = similar(base_sub.events[index].text,
                                                  dialogue_sub.events[index+offset+iteration].text)
                        # One of the next events in our dialogue_sub matches the
                        # current base_sub event, meaning the dialogue_sub has
                        # additional events that need to be copied to base_sub
                        if copy_similarity > 0.6:
                            for copy_index in range(iteration):
                                copy_indices.add(index+offset+copy_index)
                                print(" + ",
                                      dialogue_sub.events[index+offset+copy_index].dump_with_type())
                            offset += iteration
                            comparison_problem = False
                            break
                if comparison_problem:
                    for iteration in range(lookahead):
                        del_similarity = similar(base_sub.events[index+iteration].text,
                                                 dialogue_sub.events[index+offset].text)
                        if del_similarity > 0.6:
                            # One of the next events in our base_sub matches current dialogue_sub
                            # event, meaning base_sub has additional events that need to be removed
                            delete_indices.add(index)
                            offset -= 1
                            print(" - ",
                                  base_sub.events[index].dump_with_type())
                            comparison_problem = False
                            break

                # It is possible that comparison_problem is still True here, but that
                # only means that there is an issue with the next line as well. So,
                # nothing to do here anymore.

        return (delete_indices, copy_indices)

    def merge(self, base_subtitle_input: str,
              dialogue_subtitle_input: str, output_file: str) -> None:
        """ Merge the dialogue of one subtitle into another subtitle """
        with open(base_subtitle_input, encoding='utf_8_sig') as file:
            base_subtitle = ass.parse(file)
        with open(dialogue_subtitle_input, encoding='utf_8_sig') as file:
            dialogue_subtitle = ass.parse(file)

        # Create sorted copies that hold only dialogue (or all other events)
        base_subtitle_d = copy.deepcopy(base_subtitle)
        base_subtitle.events = self.__remove_dialogue(base_subtitle.events)
        base_subtitle_d.events = self.__sort_subtitle_events(
            self.__keep_dialogue(base_subtitle_d.events))
        dialogue_subtitle_d = copy.deepcopy(dialogue_subtitle)
        dialogue_subtitle_d.events = self.__sort_subtitle_events(
            self.__keep_dialogue(dialogue_subtitle_d.events))

        # Detect changes needed for merging dialogue
        event_changes = self.__find_events_misalignments(
            base_subtitle_d, dialogue_subtitle_d)

        if len(event_changes[0]) > 0 or len(event_changes[1]) > 0:
            # If there are any changes required, we print out the file names
            # so that the user knows to which files the changes apply.
            print(os.path.basename(base_subtitle_input), " | ",
                  os.path.basename(dialogue_subtitle_input))
            print()

        delete_indices_from_list(event_changes[0], base_subtitle_d.events)

        # Storing the events that we need to copy separately to prevent event misalignment
        # in the case the timing between subtitle files is relatively large. Also allowing
        # for an easier way to log to the user which subtitles need to be manually re-timed.
        move_events = []
        move_indices_list_to_list(
            event_changes[1], move_events, dialogue_subtitle_d.events)

        if self.export_dialogue_changes:
            with open(output_file + '.log', 'w', encoding='utf_8_sig') as log_file:
                # Copy dialogue changes from our dialogue subtitle to the base subtitle.
                for (base_event, dialogue_event) in \
                        zip(base_subtitle_d.events, dialogue_subtitle_d.events):
                    # Logging it to file so we can later look at the changes
                    log_file.write(
                        f"{base_event.text} => {dialogue_event.text}\n")
                    base_event.text = dialogue_event.text
                    base_event.style = dialogue_event.style

        # Sort and combine the dialogue events, move_events, and the rest of the events.
        base_subtitle.events = sorted(
            [*base_subtitle.events, *base_subtitle_d.events, *move_events], key=lambda e: e.start)

        # Export subtitle
        with open(output_file, "w", encoding='utf_8_sig') as file:
            base_subtitle.dump_file(file)
