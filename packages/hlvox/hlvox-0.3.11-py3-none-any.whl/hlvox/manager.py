"""Manages multiple voices
"""
import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union

from hlvox.voice import MultiVoice, SingleVoice, Voice

log = logging.getLogger(__name__)


class DuplicateVoice(Exception):
    """Raised when duplicate voices are found
    """


class Manager:
    """Manages multiple voices
    """

    def __init__(self, voices_path: Union[Path, str], databases_path: Union[Path, str]):
        self.voices_path = Path(voices_path)
        self.dbs_path = Path(databases_path)
        # This strangeness is to make mypy happy. There is probably a cleaner way to do it.
        single_voices = self._load_voices(self.voices_path)
        multi_voice = self._create_multi_voice(single_voices)
        voices: Dict[str, Union[MultiVoice, SingleVoice]] = {}
        voices.update(single_voices)
        voices['multi'] = multi_voice
        self.voices = voices

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.exit()

    def _create_db_path(self, databases_path: Path, voice_name: str) -> Path:
        db_path = databases_path / voice_name
        db_path.mkdir(parents=True, exist_ok=True)
        return db_path

    def _load_voices(self, path: Path) -> Dict[str, SingleVoice]:
        voices = {}
        voice_folders = list(x for x in path.iterdir() if x.is_dir())
        for voice_folder in voice_folders:
            voice_name = voice_folder.name.lower()
            if voice_name in voices:
                raise DuplicateVoice('Duplicate voice name found')
            db_path = self._create_db_path(
                databases_path=self.dbs_path, voice_name=voice_folder.name)
            new_voice = SingleVoice(
                name=voice_name, path=voice_folder, database_path=db_path)
            voices[new_voice.name] = new_voice
        return voices

    def _create_multi_voice(self, voices: Dict[str, SingleVoice]) -> MultiVoice:
        db_path = self._create_db_path(
            databases_path=self.dbs_path, voice_name='multi')
        return MultiVoice(
            voices=voices,
            database_path=db_path,
        )

    def get_voice_names(self) -> List[str]:
        """Gets names of available voices

        Returns:
            list -- list of voice name strings
        """

        voice_names = list(self.voices.keys())
        voice_names.sort()
        return voice_names

    def get_voice(self, name: str) -> Optional[Voice]:
        """Get voice of requested name

        Args:
            name ({string}): name of voice to get

        Returns:
            {voxvoice}: requested voice
        """
        if name in self.voices:
            return self.voices[name]
        return None

    def exit(self):
        """Exit all loaded voices
        """
        for voice in self.voices.values():
            voice.exit()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(
        description='Generate a sentence using voices')
    parser.add_argument('-s', '--voices-dir', type=str, required=True,
                        help='Path to folder with voice audio file folders')
    parser.add_argument('-d', '--db', type=str, required=True,
                        help='Path to store database files')
    parser.add_argument('-f', '--format', type=str, required=False,
                        default='wav', help='Audio format to export as')
    parser.add_argument('voice', type=str)
    parser.add_argument('sentence', type=str)
    args = parser.parse_args()

    voices_dir = Path(args.voices_dir)
    if not voices_dir.is_dir():
        log.error('Voices dir at %s does not exist!', voices_dir)
        sys.exit(1)

    dbs_path = Path(args.db)

    manager = Manager(
        voices_path=voices_dir,
        databases_path=dbs_path,
    )

    loaded_voice = manager.get_voice(args.voice)
    if loaded_voice is None:
        log.error("Voice %s was not found", loaded_voice)
        sys.exit(1)

    sentence = loaded_voice.generate_audio(args.sentence)
    if sentence is None or sentence.audio is None:
        log.error('Cannot generate %s: %s', sentence.sentence, sentence)
        sys.exit(1)

    # Paths can't have : in them, so replace with % as a stand-in
    sanitized_sentence = sentence.sentence.replace(':', '%')
    output_path = Path.cwd().joinpath(f"{sanitized_sentence}.{args.format}")

    log.info('Exporting to %s', output_path)
    sentence.audio.export(output_path, format=args.format)
