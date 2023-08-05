"""Abilities"""

from enum import Enum, Flag, auto
from typing import Mapping, Protocol, TypeVar


class Permissions(Flag):
    """Ability Permissions"""

    OPTION = auto()
    WRITE = auto()
    READ = auto()


_T = TypeVar("_T")


class Capability(Protocol[_T]):
    """Capability"""

    value: _T
    permissions: Permissions


class CloudStorage(Flag):
    """Cloud Storage Capabilities"""

    UPLOAD = auto()
    CONFIG = auto()
    DEPLOY = auto()


class DayNight(Enum):
    """Day/Night"""

    DAY_NIGHT = auto()
    THRESHOLD = auto()


class DDns(Enum):
    """DDNS"""

    SWAN = auto()
    THREE322 = auto()
    """3322"""
    DYNDNS = auto()
    SWAN_3322 = auto()
    """swan and 3322"""
    SWAN_DYNDNS = auto()
    DYNDNS_3322 = auto()
    """DynDns and 3322"""
    SWAN_DYNDNS_3322 = auto()
    """swan, DynDns, and 3322"""
    NOIP = auto()
    DYNDNS_NOIP = auto()


class Email(Enum):
    """Email"""

    JPEG = auto()
    """Supports JPEG attachments"""
    VIDEO_JPEG = auto()
    """Supports video and JPEG attachments"""
    VIDEO_JPEG_NICK = auto()
    """Supports video and JPEG attachments and sender nickname"""


class EncodingType(Enum):
    """Encoding Type"""

    H264 = auto()
    H265 = auto()


class FloodLight(Enum):
    """Flood Light"""

    WHITE = auto()
    AUTO = auto()


class Ftp(Enum):
    """FTP"""

    STREAM = auto()
    JPEG_STREAM = auto()
    MODE = auto()
    JPEG_STREAM_MODE = auto()
    STREAM_MODE_TYPE = auto()
    JPEG_STREAM_MODE_TYPE = auto()


class Live(Enum):
    """Live"""

    MAIN_EXTERN_SUB = auto()
    MAIN_SUB = auto()


class Osd(Enum):
    """Osd"""

    SUPPORTED = auto()
    DISTINCT = auto()


class PTZControl(Enum):
    """PTZ Control"""

    ZOOM = auto()
    ZOOM_FOCUS = auto()
    """Zoom and Focus"""


class PTZDirection(Enum):
    """PTZ Direction"""

    EIGHT_AUTO = auto()
    """8 directions with auto scan"""
    FOUR_NO_AUTO = auto()
    """4 directions, no auto scan"""


class PTZType(Enum):
    """PTZ Type"""

    AF = auto()
    """Auto Focus"""
    PTZ = auto()
    """Pan Tilt Zoom"""
    PT = auto()
    """Pan Tilt"""
    BALL = auto()
    PTZ_NO_SPEED = auto()
    """Pan Tilt Zoom, no speed control"""


class RecordSchedule(Enum):
    """Record Schedule"""

    MOTION = auto()
    MOTION_LIVE = auto()
    """Motion detection and normal recording"""


class ScheduleVersion(Enum):
    """Schedule Version"""

    BASIC = auto()
    V20 = auto()
    "v2.0"


class Time(Enum):
    """Time"""

    SUNDAY = auto()
    ANYDAY = auto()


class Upgrade(Enum):
    """Upgrade"""

    MANUAL = auto()
    ONLINE = auto()


class VideoClip(Enum):
    """Video Clip"""

    FIXED = auto()
    MOD = auto()


class ChannelCapabilities(Protocol):
    """Channel User Capabilities"""

    class AI(Protocol):
        """AI"""

        class Track(Capability[bool], Protocol):
            """Track"""

            pet: Capability[bool]

        track: Track

    ai: AI

    class Alarm(Protocol):
        """Alarm"""

        audio: Capability[bool]
        io_in: Capability[bool]
        io_out: Capability[bool]
        motion: Capability[bool]
        rf: Capability[bool]

    alarm: Alarm
    battery: Capability[bool]
    battery_analysis: Capability[bool]
    camera_mode: Capability[bool]
    disable_autofocus: Capability[bool]
    enc: Capability[bool]
    floodlight: Capability[FloodLight]
    ftp: Capability[Ftp]
    image: Capability[bool]
    indicator_light: Capability[bool]

    class ISP(Capability[bool], Protocol):
        """ISP"""

        threeDnr: Capability[bool]
        antiflicker: Capability[bool]
        backlight: Capability[bool]
        bright: Capability[bool]
        contrast: Capability[bool]
        day_night: Capability[DayNight]
        exposure_mode: Capability[bool]
        flip: Capability[bool]
        hue: Capability[bool]
        mirror: Capability[bool]
        satruation: Capability[bool]
        sharpen: Capability[bool]
        white_balance: Capability[bool]

    isp: ISP
    led_control: Capability[bool]
    live: Capability[Live]
    main_encoding: Capability[EncodingType]
    mask: Capability[bool]

    class MD(Protocol):
        """MotionDetection"""

        class Trigger(Protocol):
            """Trigger"""

            audio: Capability[bool]
            record: Capability[bool]

        trigger: Trigger
        with_pir: Capability[bool]

    motion_detection: MD

    osd: Capability[Osd]
    power_led: Capability[bool]

    class PTZ(Protocol):
        """PTZ"""

        control: Capability[PTZControl]
        direction: Capability[PTZDirection]
        patrol: Capability[bool]
        preset: Capability[bool]
        tattern: Capability[bool]
        type: Capability[PTZType]

    ptz: PTZ

    class Record(Protocol):
        """Record"""

        config: Capability[bool]
        download: Capability[bool]
        replay: Capability[bool]
        schedule: Capability[RecordSchedule]

    record: Record

    shelter_config: Capability[bool]
    snap: Capability[bool]

    class Supports(Protocol):
        """Supports"""

        class AI(Capability[bool], Protocol):
            """AI"""

            animal: Capability[bool]
            detect_config: Capability[bool]
            pet: Capability[bool]
            face: Capability[bool]
            people: Capability[bool]
            sensitivity: Capability[bool]
            stay_time: Capability[bool]
            target_size: Capability[bool]
            track_classify: Capability[bool]
            vehicle: Capability[bool]
            adjust: Capability[bool]

        ai: AI

        class FloodLight(Protocol):
            """FloodLight"""

            brightness: Capability[bool]
            intelligent: Capability[bool]
            keep_on: Capability[bool]
            schedule: Capability[bool]
            switch: Capability[bool]

        flood_light: FloodLight

        gop: Capability[bool]
        motion_detection: Capability[bool]
        ptz_check: Capability[bool]
        threshold_adjust: Capability[bool]
        white_dark: Capability[bool]

    supports: Supports
    video_clip: Capability[VideoClip]
    watermark: Capability[bool]
    white_balance: Capability[bool]


class Capabilities(Protocol):
    """Device User Capabilities"""

    three_g: Capability[bool]
    channels: Mapping[int, ChannelCapabilities]

    class Alarm(Protocol):
        """Alarm"""

        audio: Capability[bool]
        disconnect: Capability[bool]

        class HDD(Protocol):
            """HDDD"""

            error: Capability[bool]
            full: Capability[bool]

        hdd: HDD

        ip_conflict: Capability[bool]

    alarm: Alarm

    auth: Capability[bool]
    auto_maintenance: Capability[bool]
    cloud_storage: Capability[CloudStorage]
    custom_audio: Capability[bool]
    date_format: Capability[bool]
    ddns: Capability[DDns]

    class Device(Protocol):
        """Device"""

        info: Capability[bool]
        name: Capability[bool]

    device: Device

    disable_autofocus: Capability[bool]
    disk: Capability[bool]
    display: Capability[bool]

    class Email(Capability[Email], Protocol):
        """Email"""

        interval: Capability[bool]
        schedule: Capability[bool]

    email: Email

    config: Capability[bool]
    config_import: Capability[bool]
    config_export: Capability[bool]

    class FTP(Protocol):
        """FTP"""

        auto_dir: Capability[bool]

        class Stream(Protocol):
            """Stream"""

            ext: Capability[bool]
            sub: Capability[bool]

        stream: Stream
        picture: Capability[bool]
        test: Capability[bool]

    ftp: FTP

    hour_format: Capability[bool]
    """change hour format supported"""

    http: Capability[bool]
    http_flv: Capability[bool]
    https: Capability[bool]
    ipc_manager: Capability[bool]
    led_control: Capability[bool]
    local_link: Capability[bool]
    log: Capability[bool]
    media_port: Capability[bool]
    ntp: Capability[bool]
    online: Capability[bool]
    onvif: Capability[bool]
    p2p: Capability[bool]
    performance: Capability[bool]
    pppoe: Capability[bool]
    push: Capability[bool]
    push_schedule: Capability[bool]
    reboot: Capability[bool]

    class Record(Protocol):
        """Record"""

        extension_time_list: Capability[bool]
        overwrite: Capability[bool]
        pack_duration: Capability[bool]
        pre_record: Capability[bool]

    record: Record
    restore: Capability[bool]
    rtmp: Capability[bool]
    rtsp: Capability[bool]
    schedule_version: Capability[ScheduleVersion]
    sd_card: Capability[bool]
    show_qr_code: Capability[bool]
    sim_module: Capability[bool]

    class Supports(Protocol):
        """Supports"""

        class Audio(Protocol):
            """Audio"""

            class Alarm(Protocol):
                """Alarm"""

                enable: Capability[bool]
                schedule: Capability[bool]
                task_enable: Capability[bool]

            alarm: Alarm

        audio: Audio

        class Buzzer(Capability[bool], Protocol):
            """Buzzer"""

            class Task(Capability[bool], Protocol):
                """Task"""

                enable: Capability[bool]

            task: Task

        buzzer: Buzzer

        class Email(Protocol):
            """Email"""

            enable: Capability[bool]
            task_enable: Capability[bool]

        email: Email

        class FTP(Protocol):
            """FTP"""

            class Cover(Protocol):
                """Cover"""

                picture: Capability[bool]
                video: Capability[bool]

            cover: Cover

            dir_YM: Capability[bool]
            enable: Capability[bool]

            class Picture(Protocol):
                """Picture"""

                capture_mode: Capability[bool]
                custom_resolution: Capability[bool]
                swap: Capability[bool]

            picture: Picture

            class Task(Capability[bool], Protocol):
                """Task"""

                enable: Capability[bool]

            task: Task
            video_swap: Capability[bool]
            ftps_encrypt: Capability[bool]

        ftp: FTP

        http_enable: Capability[bool]
        https_enable: Capability[bool]
        onvif_enable: Capability[bool]
        push_interval: Capability[bool]

        class Record(Protocol):
            """Record"""

            schedule_enable: Capability[bool]
            enable: Capability[bool]

        record: Record

        rtmp_enable: Capability[bool]
        rtsp_enable: Capability[bool]

    supports: Supports
    talk: Capability[bool]
    time: Capability[Time]
    tv_system: Capability[bool]
    upgrade: Capability[Upgrade]
    upnp: Capability[bool]
    user: Capability[bool]
    video_clip: Capability[VideoClip]

    class Wifi(Capability[bool], Protocol):
        """WIFI"""

        testable: Capability[bool]

    wifi: Wifi
