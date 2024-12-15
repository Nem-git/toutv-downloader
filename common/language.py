
import pycountry

from common.audio import Audio


class Language:

    def Fix(self, audio: Audio, country: str) -> str:

        new_audio_language: str = ""
        language_code: str
        country_code: str

        try:
            language_code = pycountry.languages.lookup(audio.language).alpha_2
        except:
            try:
                language_code = pycountry.languages.lookup(audio.language[:2]).alpha_2
            except:
                language_code = "und"
        
        new_audio_language += language_code.lower()

        try:
            country_code = pycountry.countries.lookup(country).alpha_2
        except:
            try:
                country_code = pycountry.countries.lookup(country[:2]).alpha_2
            except:
                country_code = ""
        
        new_audio_language += f"-{country_code.upper()}"
        
        audio.language = new_audio_language

        return new_audio_language