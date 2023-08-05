import sys
from typing import Any, overload
from typing_extensions import Literal

if sys.platform != "win32" and sys.platform != "darwin":
    AFMT_AC3: int
    AFMT_A_LAW: int
    AFMT_IMA_ADPCM: int
    AFMT_MPEG: int
    AFMT_MU_LAW: int
    AFMT_QUERY: int
    AFMT_S16_BE: int
    AFMT_S16_LE: int
    AFMT_S16_NE: int
    AFMT_S8: int
    AFMT_U16_BE: int
    AFMT_U16_LE: int
    AFMT_U8: int
    SNDCTL_COPR_HALT: int
    SNDCTL_COPR_LOAD: int
    SNDCTL_COPR_RCODE: int
    SNDCTL_COPR_RCVMSG: int
    SNDCTL_COPR_RDATA: int
    SNDCTL_COPR_RESET: int
    SNDCTL_COPR_RUN: int
    SNDCTL_COPR_SENDMSG: int
    SNDCTL_COPR_WCODE: int
    SNDCTL_COPR_WDATA: int
    SNDCTL_DSP_BIND_CHANNEL: int
    SNDCTL_DSP_CHANNELS: int
    SNDCTL_DSP_GETBLKSIZE: int
    SNDCTL_DSP_GETCAPS: int
    SNDCTL_DSP_GETCHANNELMASK: int
    SNDCTL_DSP_GETFMTS: int
    SNDCTL_DSP_GETIPTR: int
    SNDCTL_DSP_GETISPACE: int
    SNDCTL_DSP_GETODELAY: int
    SNDCTL_DSP_GETOPTR: int
    SNDCTL_DSP_GETOSPACE: int
    SNDCTL_DSP_GETSPDIF: int
    SNDCTL_DSP_GETTRIGGER: int
    SNDCTL_DSP_MAPINBUF: int
    SNDCTL_DSP_MAPOUTBUF: int
    SNDCTL_DSP_NONBLOCK: int
    SNDCTL_DSP_POST: int
    SNDCTL_DSP_PROFILE: int
    SNDCTL_DSP_RESET: int
    SNDCTL_DSP_SAMPLESIZE: int
    SNDCTL_DSP_SETDUPLEX: int
    SNDCTL_DSP_SETFMT: int
    SNDCTL_DSP_SETFRAGMENT: int
    SNDCTL_DSP_SETSPDIF: int
    SNDCTL_DSP_SETSYNCRO: int
    SNDCTL_DSP_SETTRIGGER: int
    SNDCTL_DSP_SPEED: int
    SNDCTL_DSP_STEREO: int
    SNDCTL_DSP_SUBDIVIDE: int
    SNDCTL_DSP_SYNC: int
    SNDCTL_FM_4OP_ENABLE: int
    SNDCTL_FM_LOAD_INSTR: int
    SNDCTL_MIDI_INFO: int
    SNDCTL_MIDI_MPUCMD: int
    SNDCTL_MIDI_MPUMODE: int
    SNDCTL_MIDI_PRETIME: int
    SNDCTL_SEQ_CTRLRATE: int
    SNDCTL_SEQ_GETINCOUNT: int
    SNDCTL_SEQ_GETOUTCOUNT: int
    SNDCTL_SEQ_GETTIME: int
    SNDCTL_SEQ_NRMIDIS: int
    SNDCTL_SEQ_NRSYNTHS: int
    SNDCTL_SEQ_OUTOFBAND: int
    SNDCTL_SEQ_PANIC: int
    SNDCTL_SEQ_PERCMODE: int
    SNDCTL_SEQ_RESET: int
    SNDCTL_SEQ_RESETSAMPLES: int
    SNDCTL_SEQ_SYNC: int
    SNDCTL_SEQ_TESTMIDI: int
    SNDCTL_SEQ_THRESHOLD: int
    SNDCTL_SYNTH_CONTROL: int
    SNDCTL_SYNTH_ID: int
    SNDCTL_SYNTH_INFO: int
    SNDCTL_SYNTH_MEMAVL: int
    SNDCTL_SYNTH_REMOVESAMPLE: int
    SNDCTL_TMR_CONTINUE: int
    SNDCTL_TMR_METRONOME: int
    SNDCTL_TMR_SELECT: int
    SNDCTL_TMR_SOURCE: int
    SNDCTL_TMR_START: int
    SNDCTL_TMR_STOP: int
    SNDCTL_TMR_TEMPO: int
    SNDCTL_TMR_TIMEBASE: int
    SOUND_MIXER_ALTPCM: int
    SOUND_MIXER_BASS: int
    SOUND_MIXER_CD: int
    SOUND_MIXER_DIGITAL1: int
    SOUND_MIXER_DIGITAL2: int
    SOUND_MIXER_DIGITAL3: int
    SOUND_MIXER_IGAIN: int
    SOUND_MIXER_IMIX: int
    SOUND_MIXER_LINE: int
    SOUND_MIXER_LINE1: int
    SOUND_MIXER_LINE2: int
    SOUND_MIXER_LINE3: int
    SOUND_MIXER_MIC: int
    SOUND_MIXER_MONITOR: int
    SOUND_MIXER_NRDEVICES: int
    SOUND_MIXER_OGAIN: int
    SOUND_MIXER_PCM: int
    SOUND_MIXER_PHONEIN: int
    SOUND_MIXER_PHONEOUT: int
    SOUND_MIXER_RADIO: int
    SOUND_MIXER_RECLEV: int
    SOUND_MIXER_SPEAKER: int
    SOUND_MIXER_SYNTH: int
    SOUND_MIXER_TREBLE: int
    SOUND_MIXER_VIDEO: int
    SOUND_MIXER_VOLUME: int

    control_labels: list[str]
    control_names: list[str]

    # TODO: oss_audio_device return type
    @overload
    def open(mode: Literal["r", "w", "rw"]) -> Any: ...
    @overload
    def open(device: str, mode: Literal["r", "w", "rw"]) -> Any: ...

    # TODO: oss_mixer_device return type
    def openmixer(device: str = ...) -> Any: ...

    class OSSAudioError(Exception): ...
    error = OSSAudioError
