from typing import Iterable, Optional

import more_itertools
from elftools.construct import Container
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import NoteSection
from elftools.elf.segments import NoteSegment

# FIXME: Deduplicate. Copy pasta from elf_utils.py

NT_GNU_BUILD_ID = "NT_GNU_BUILD_ID"

ELF_NOTE_SECTION_OWNER_GNU = "GNU"


def get_note_segments(elf: ELFFile) -> Iterable[NoteSegment]:
    return filter(lambda segment: isinstance(segment, NoteSegment), elf.iter_segments())


def get_note_sections(elf: ELFFile) -> Iterable[NoteSection]:
    return filter(lambda segment: isinstance(segment, NoteSection), elf.iter_sections())


def get_notes(elf: ELFFile) -> Iterable[Container]:
    for note_segment in get_note_segments(elf):
        yield from note_segment.iter_notes()
    for note_section in get_note_sections(elf):
        yield from note_section.iter_notes()


def is_gnu_build_id_note_section(section: NoteSection) -> bool:
    return (section.n_type == NT_GNU_BUILD_ID) and (section.n_name == ELF_NOTE_SECTION_OWNER_GNU)


def get_gnu_build_id(elf: ELFFile) -> Optional[str]:
    build_id_note = more_itertools.first_true(
        get_notes(elf),
        pred=is_gnu_build_id_note_section,
    )
    if not build_id_note:
        return None
    return build_id_note.n_desc
