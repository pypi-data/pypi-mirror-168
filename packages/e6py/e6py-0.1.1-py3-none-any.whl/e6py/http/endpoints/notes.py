from typing import Any, List

from e6py.http.route import Route
from e6py.models.note import Note
from e6py.models.tag import Tag


class NoteRequests:
    request: Any

    def get_notes(
        self,
        body: str = None,
        post_id: int = None,
        creator_name: str = None,
        creator_id: int = None,
        is_active: bool = None,
        post_tags_match: Tag | str | List[str | Tag] = None,
        page: int = None,
        before: int = None,
        after: int = None,
        limit: int = 75,
    ) -> List[Note] | None:
        """
        Get notes with specified arguments

        Args:
            body: Note body, use `*` for wildcard
            post_id: Post to get notes from
            creator_name: Name of creator
            creator_id: ID of creator
            is_active: If note is active
            post_tags_match: List of tags to limit search to
            page: Page number, max 750
            before:  Get posts before this post, overrides page
            after: Get posts after this post, overrides before
            limit: Number of notes to get, max 320

        Returns:
            List of notes if any found

        Raises:
            ValueError: Too high of limit
        """
        if before:
            page = f"b{before}"
        elif after:
            page = f"a{after}"
        elif not page:
            page = 0
        elif page > 750:
            raise ValueError("Page must be < 750, consider using 'before'")
        if limit > 320:
            raise ValueError("Limit must be <= 320")

        if post_tags_match and isinstance(post_tags_match, list):
            post_tags_match = "+".join([tag.name if isinstance(tag, Tag) else tag for tag in post_tags_match])
        elif post_tags_match and isinstance(post_tags_match, Tag):
            post_tags_match = post_tags_match.name
        elif post_tags_match and isinstance(post_tags_match, str):
            post_tags_match = post_tags_match.replace(" ", "+")

        data = self.request(
            Route("GET", "/notes.json"),
            search__body_matches=body,
            search__post_id=post_id,
            search__creator_name=creator_name,
            search__creator_id=creator_id,
            search__is_active=is_active,
            search__post_tags_match=post_tags_match,
            limit=limit,
            page=page,
        )

        notes = Note.from_list(data, self) if data else None
        if self.cache and notes:
            for note in notes:
                self._note_cache[note.id] = note
        return notes

    def get_note(self, note_id: int) -> Note | None:
        """
        Get specified note.

        Args:
            note_id: ID of note to get

        Returns:
            Specified note if it exists
        """
        if self.cache and (note := self._note_cache.get(note_id)):
            return note
        data = self.request(Route("GET", f"/notes/{note_id}.json"))
        note = Note.from_dict(data, self) if data else None
        if self.cache:
            self._note_cache[note_id] = note
        return note
