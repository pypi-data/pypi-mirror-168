# Models taken from pyteledantic:
# https://github.com/isys35/pyteledantic/blob/03ca79a6af049c7e98245e42daa2c18d4629e003/pyteledantic/models.py
# 
# License for this file: Apache License 2.0 (see the bottom of this file).
# Programmer: https://github.com/isys35

from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field, validator


class Bot(BaseModel):
    """
    Contains your bot token
    """
    token: str


class User(BaseModel):
    """
    https://core.telegram.org/bots/api#user
    This object represents a Telegram user or bot.
    """
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None


class ChatPhoto(BaseModel):
    """
    https://core.telegram.org/bots/api#chatphoto
    This object represents a chat photo.
    """
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str


class ChatPermissions(BaseModel):
    """
    https://core.telegram.org/bots/api#chatpermissions
    Describes actions that a non-administrator user
    is allowed to take in a chat.
    """
    can_send_messages: Optional[bool] = None
    can_send_media_messages: Optional[bool] = None
    can_send_polls: Optional[bool] = None
    can_send_other_messages: Optional[bool] = None
    can_add_web_page_previews: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None


class Location(BaseModel):
    """
    https://core.telegram.org/bots/api#location
    This object represents a point on the map.
    """
    longitude: float
    latitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None

    @validator('horizontal_accuracy')
    def size_horizontal_accuracy_must_contain_a_range(cls, v):
        if v < 0 or v > 1500:
            raise ValueError('Must contain a range of 0 - 1500')


class ChatLocation(BaseModel):
    """
    https://core.telegram.org/bots/api#chatlocation
    Represents a location to which a chat is connected.
    """
    location: Location
    address: str


class Chat(BaseModel):
    """
    https://core.telegram.org/bots/api#chat
    This object represents a chat.
    """
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo: Optional[ChatPhoto] = None
    bio: Optional[str] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional['Message'] = None
    permissions: Optional[ChatPermissions] = None
    slow_mode_delay: Optional[int] = None
    message_auto_delete_time: Optional[int] = None
    sticker_set_name: Optional[str] = None
    can_set_sticker_set: Optional[bool] = None
    linked_chat_id: Optional[int] = None
    location: Optional[ChatLocation] = None


class MessageEntity(BaseModel):
    """
    https://core.telegram.org/bots/api#messageentity
    This object represents one special entity in a text message.
     For example, hashtags, usernames, URLs, etc.
    """
    type: str
    offset: int
    length: int
    url: Optional[str] = None
    user: Optional[User] = None
    language: Optional[str] = None


class PhotoSize(BaseModel):
    """
    https://core.telegram.org/bots/api#photosize
    This object represents one size of a photo or a file / sticker thumbnail.
    """
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int] = None


class Animation(BaseModel):
    """
    https://core.telegram.org/bots/api#animation
    This object represents an animation file
    (GIF or H.264/MPEG-4 AVC video without sound).
    """
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class Audio(BaseModel):
    """
    https://core.telegram.org/bots/api#audio
    This object represents an audio file
    to be treated as music by the Telegram clients.
    """
    file_id: str
    file_unique_id: str
    duration: int
    performer: Optional[str] = None
    title: Optional[str] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    thumb: Optional[PhotoSize] = None


class Document(BaseModel):
    """
    https://core.telegram.org/bots/api#document
    This object represents a general file
    (as opposed to photos, voice messages and audio files).
    """
    file_id: str
    file_unique_id: str
    thumb: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class Sticker(BaseModel):
    """
    https://core.telegram.org/bots/api#sticker
    This object represents a sticker.
    """
    file_id: str
    file_unique_id: str
    width: int
    height: int
    is_animated: bool
    thumb: Optional[PhotoSize] = None
    emoji: Optional[str] = None
    set_name: Optional[str] = None
    mask_position: Optional[str] = None
    file_size: Optional[int] = None


class Video(BaseModel):
    """
    https://core.telegram.org/bots/api#video
    This object represents a video file.
    """
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class VideoNote(BaseModel):
    """
    https://core.telegram.org/bots/api#videonote
    This object represents a video message
    (available in Telegram apps as of v.4.0).
    """
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumb: Optional[PhotoSize] = None
    file_size: Optional[int] = None


class Voice(BaseModel):
    """
    https://core.telegram.org/bots/api#voice
    This object represents a voice note.
    """
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class Contact(BaseModel):
    """
    https://core.telegram.org/bots/api#contact
    This object represents a phone contact.
    """
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    user_id: Optional[str] = None
    vcard: Optional[str] = None


class Dice(BaseModel):
    """
    https://core.telegram.org/bots/api#dice
    This object represents an animated emoji that displays a random value.
    """
    emoji: str
    value: int


class Game(BaseModel):
    """
    https://core.telegram.org/bots/api#game
    This object represents a game.
    Use BotFather to create and edit games,
    their short names will act as unique identifiers.
    """
    title: str
    description: str
    photo: Union[list, PhotoSize, None] = None
    text: Optional[str] = None
    text_entities: Union[list, MessageEntity, None] = None
    animation: Optional[Animation] = None


class PollOption(BaseModel):
    """
    https://core.telegram.org/bots/api#polloption
    This object contains information about one answer option in a poll.
    """
    text: str
    voter_count: int


class Poll(BaseModel):
    """
    https://core.telegram.org/bots/api#poll
    This object contains information about a poll.
    """
    id: str
    question: str
    options: Union[list, PollOption, None] = None
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    correct_option_id: Optional[int] = None
    explanation: Optional[str] = None
    explanation_entities: Union[list, MessageEntity, None] = None
    open_period: Optional[int] = None
    close_date: Optional[int] = None

    @validator('question')
    def question_characters_limit(cls, v):
        if len(v) > 300:
            raise ValueError('question limited 300 characters')


class MessageAutoDeleteTimerChanged(BaseModel):
    """
    https://core.telegram.org/bots/api#messageautodeletetimerchanged
    This object represents a service message
    about a change in auto-delete timer settings.
    """
    message_auto_delete_time: int


class Venue(BaseModel):
    """
    https://core.telegram.org/bots/api#venue
    This object represents a venue.
    """
    location: Location
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None


class Invoice(BaseModel):
    """
    https://core.telegram.org/bots/api#invoice
    This object contains basic information about an invoice.
    """
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


class ShippingAddress(BaseModel):
    """
    https://core.telegram.org/bots/api#shippingaddress
    This object represents a shipping address.
    """
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


class OrderInfo(BaseModel):
    """
    https://core.telegram.org/bots/api#orderinfo
    This object represents information about an order.
    """
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    shipping_address: Optional[ShippingAddress] = None


class SuccessfulPayment(BaseModel):
    """
    https://core.telegram.org/bots/api#successfulpayment
    This object contains basic information about a successful payment.
    """
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None
    telegram_payment_charge_id: str
    provider_payment_charge_id: str


class PassportFile(BaseModel):
    """
    https://core.telegram.org/bots/api#passportfile
    This object represents a file uploaded to Telegram Passport.
     Currently all Telegram Passport files are in JPEG
     format when decrypted and don't exceed 10MB.
    """
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int


class EncryptedPassportElement(BaseModel):
    """
    https://core.telegram.org/bots/api#encryptedpassportelement
    Contains information about documents or
    other Telegram Passport elements shared with the bot by the user.
    """
    type: str
    data: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    files: Union[list, PassportFile, None] = None
    front_side: Optional[PassportFile] = None
    reverse_side: Optional[PassportFile] = None
    selfie: Optional[PassportFile] = None
    translation: Union[list, PassportFile, None] = None
    hash: str


class EncryptedCredentials(BaseModel):
    """
    https://core.telegram.org/bots/api#encryptedcredentials
    Contains data required for decrypting
    and authenticating EncryptedPassportElement.
    See the Telegram Passport Documentation
    for a complete description of the data decryption
    and authentication processes.
    """
    data: str
    hash: str
    secret: str


class PassportData(BaseModel):
    """
    https://core.telegram.org/bots/api#passportdata
    Contains information
    about Telegram Passport data shared with the bot by the user.
    """
    data: Union[list, EncryptedPassportElement]
    credentials: EncryptedCredentials


class ProximityAlertTriggered(BaseModel):
    """
    https://core.telegram.org/bots/api#proximityalerttriggered
    This object represents the content of a service message,
    sent whenever a user in the chat triggers a proximity
    alert set by another user.
    """
    traveler: User
    watcher: User
    distance: int


class VoiceChatScheduled(BaseModel):
    """
    https://core.telegram.org/bots/api#voicechatscheduled
    This object represents the content of a service message,
    sent whenever a user in the chat triggers
     a proximity alert set by another user.
    """
    start_date: int


class VoiceChatStarted(BaseModel):
    """
    https://core.telegram.org/bots/api#voicechatstarted
    This object represents a service message
     about a voice chat started in the chat.
     Currently holds no information.
    """
    pass


class VoiceChatEnded(BaseModel):
    """
    https://core.telegram.org/bots/api#voicechatended
    This object represents a service message
    about a voice chat ended in the chat.
    """
    duration: int


class VoiceChatParticipantsInvited(BaseModel):
    """
    https://core.telegram.org/bots/api#voicechatparticipantsinvited
    This object represents a service message
    about new members invited to a voice chat.
    """
    users: Union[list, User, None] = None


class LoginUrl(BaseModel):
    """
    https://core.telegram.org/bots/api#loginurl
    This object represents
     a parameter of the inline keyboard button
      used to automatically authorize a user.
    Serves as a great replacement for the Telegram Login Widget
    when the user is coming from Telegram.
    All the user needs to do is tap/click a button
    and confirm that they want to log in.
    """
    url: str
    forward_text: Optional[str] = None
    bot_username: Optional[str] = None
    request_write_access: Optional[bool] = None


class CallbackGame(BaseModel):
    """
    https://core.telegram.org/bots/api#callbackgame
    A placeholder, currently holds no information.
    Use BotFather to set up your game.
    """
    pass


class InlineKeyboardButton(BaseModel):
    """
    https://core.telegram.org/bots/api#inlinekeyboardbutton
    This object represents one button of an inline keyboard.
    You must use exactly one of the optional fields.
    """
    text: str
    url: Optional[str]
    login_url: Optional[LoginUrl] = None
    callback_data: Optional[str] = None
    switch_inline_query: Optional[str] = None
    switch_inline_query_current_chat: Optional[str] = None
    callback_game: Optional[CallbackGame] = None
    pay: Optional[bool]


class ForceReply(BaseModel):
    """
    https://core.telegram.org/bots/api#forcereply
    Upon receiving a message with this object,
    Telegram clients will display a reply interface to the user
    (act as if the user has selected the bot's message and tapped 'Reply')
    """
    force_reply: bool = True
    input_field_placeholder: Optional[str]
    selective: Optional[bool]


class ReplyKeyboardRemove(BaseModel):
    """
    https://core.telegram.org/bots/api#replykeyboardremove
    Upon receiving a message with this object, Telegram clients
    will remove the current custom keyboard and display
    the default letter-keyboard.
    """
    remove_keyboard: bool = True
    selective: Optional[bool]


class KeyboardButtonPollType(BaseModel):
    """
    https://core.telegram.org/bots/api#keyboardbuttonpolltype
    This object represents type of a poll, which is allowed to be
    created and sent when the corresponding button is pressed.
    """
    type: Optional[str] = None


class WebAppInfo(BaseModel):
    """
    https://core.telegram.org/bots/api#webappinfo
    Contains information about a Web App.
    """
    url: Optional[str] = None


class KeyboardButton(BaseModel):
    """
    https://core.telegram.org/bots/api#keyboardbutton
    This object represents one button of the reply keyboard.
    """
    text: str
    request_contact: Optional[bool] = None
    request_location: Optional[bool] = None
    request_poll: Optional[KeyboardButtonPollType] = None
    web_app: Optional[WebAppInfo] = None


class InlineKeyboardMarkup(BaseModel):
    """
    https://core.telegram.org/bots/api#inlinekeyboardmarkup
    This object represents an inline keyboard that appears
    right next to the message it belongs to.
    """
    inline_keyboard: Union[list, list[InlineKeyboardButton]]


class ReplyKeyboardMarkup(BaseModel):
    """
    https://core.telegram.org/bots/api#replykeyboardmarkup
    This object represents a custom keyboard with reply options
    """
    keyboard: Union[list, list[KeyboardButton]]
    resize_keyboard: Optional[bool]
    one_time_keyboard: Optional[bool]
    input_field_placeholder: Optional[str]
    selective: Optional[bool]


class MessageToSend(BaseModel):
    """
    https://core.telegram.org/bots/api#sendmessage
    Message data to use sendMessage method
    """
    chat_id: Union[str, int]
    text: str
    parse_mode: Optional[str] = None
    entities: Union[list, MessageEntity, None] = None
    disable_web_page_preview: Optional[bool] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    reply_to_message_id: Optional[int] = None
    allow_sending_without_reply: Optional[bool] = None
    reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup,
                        ReplyKeyboardRemove, ForceReply, None] = None


class Message(BaseModel):
    """
    https://core.telegram.org/bots/api#message
    This object represents a message.
    """
    message_id: int
    from_user: Optional[User] = Field(None, alias='from')
    sender_chat: Optional[Chat] = None
    date: datetime
    chat: Chat
    forward_from: Optional[User] = None
    forward_from_chat: Optional[Chat] = None
    forward_from_message_id: Optional[int] = None
    forward_signature: Optional[str] = None
    forward_sender_name: Optional[str] = None
    forward_date: Optional[int] = None
    reply_to_message: Optional['Message'] = None
    via_bot: Optional[User] = None
    edit_date: Optional[int] = None
    media_group_id: Optional[str] = None
    author_signature: Optional[str] = None
    text: Optional[str] = None
    entities: Union[list, MessageEntity, None] = None
    animation: Optional[Animation] = None
    audio: Optional[Audio] = None
    document: Optional[Document] = None
    photo: Union[list, PhotoSize, None] = None
    sticker: Optional[Sticker] = None
    video: Optional[Video] = None
    video_note: Optional[VideoNote] = None
    voice: Optional[Voice] = None
    caption: Optional[str] = None
    caption_entities: Union[list, MessageEntity, None] = None
    contact: Optional[Contact] = None
    dice: Optional[Dice] = None
    game: Optional[Game] = None
    poll: Optional[Poll] = None
    venue: Optional[Venue] = None
    location: Optional[Location] = None
    new_chat_members: Union[list, User, None] = None
    left_chat_member: Optional[User] = None
    new_chat_title: Optional[str] = None
    new_chat_photo: Union[list, PhotoSize, None] = None
    delete_chat_photo: Optional[bool] = None
    group_chat_created: Optional[bool] = None
    supergroup_chat_created: Optional[bool] = None
    channel_chat_created: Optional[bool] = None
    message_auto_delete_timer_changed: \
        Optional[MessageAutoDeleteTimerChanged] = None
    migrate_to_chat_id: Optional[int] = None
    migrate_from_chat_id: Optional[int] = None
    pinned_message: Optional['Message'] = None
    invoice: Optional[Invoice] = None
    successful_payment: Optional[SuccessfulPayment] = None
    connected_website: Optional[str] = None
    passport_data: Optional[PassportData] = None
    proximity_alert_triggered: Optional[ProximityAlertTriggered] = None
    voice_chat_scheduled: Optional[VoiceChatScheduled] = None
    voice_chat_started: Optional[VoiceChatStarted] = None
    voice_chat_ended: Optional[VoiceChatEnded] = None
    voice_chat_participants_invited: \
        Optional[VoiceChatParticipantsInvited] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None


class InlineQuery(BaseModel):
    """
    https://core.telegram.org/bots/api#inlinequery
    This object represents an incoming inline query.
     When the user sends an empty query,
     your bot could return some default or trending results.
    """
    id: str
    from_user: User = Field(alias='from')
    query: str
    offset: str
    chat_type: Optional[str] = None
    location: Optional[Location] = None

    @validator('query')
    def query_characters_limit(cls, v):
        if len(v) > 256:
            raise ValueError('query limited 256 characters')


class ChosenInlineResult(BaseModel):
    """
    https://core.telegram.org/bots/api#choseninlineresult
    Represents a result of an inline query
    that was chosen by the user and sent to their chat partner.
    """
    result_id: str
    from_user: User = Field(alias='from')
    location: Optional[Location] = None
    inline_message_id: Optional[str] = None
    query: str


class CallbackQuery(BaseModel):
    """
    https://core.telegram.org/bots/api#callbackquery
    This object represents
     an incoming callback query from a callback button
      in an inline keyboard.
    If the button that originated the query was attached
     to a message sent by the bot, the field message will be present.
    If the button was attached to a message sent
     via the bot (in inline mode),
     the field inline_message_id will be present.
    Exactly one of the fields data
    or game_short_name will be present.
    """
    id: str
    from_user: User = Field(alias='from')
    message: Optional[Message] = None
    inline_message_id: Optional[str] = None
    chat_instance: str
    data: Optional[str] = None
    game_short_name: Optional[str] = None


class ShippingQuery(BaseModel):
    """
    https://core.telegram.org/bots/api#shippingquery
    This object contains information about an incoming shipping query.
    """
    id: str
    from_user: User = Field(alias='from')
    invoice_payload: str
    shipping_address: ShippingAddress


class PreCheckoutQuery(BaseModel):
    """
    https://core.telegram.org/bots/api#precheckoutquery
    This object contains information about an incoming pre-checkout query.
    """
    id: str
    from_user: User = Field(alias='from')
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None


class PollAnswer(BaseModel):
    """
    https://core.telegram.org/bots/api#pollanswer
    This object represents an answer of a user in a non-anonymous poll.
    """
    poll_id: str
    user: User
    option_ids: Union[list, int]


class ChatMemberOwner(BaseModel):
    """
    https://core.telegram.org/bots/api#chatmemberowner
    Represents a chat member
     that owns the chat and has all administrator privileges.
    """
    status: str
    user: User
    is_anonymous: bool
    custom_title: Optional[str] = None


class ChatMemberAdministrator(BaseModel):
    """
    https://core.telegram.org/bots/api#chatmemberadministrator
    Represents a chat member that has some additional privileges.
    """
    status: str
    user: User
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_voice_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    custom_title: Optional[str] = None


class ChatMemberMember(BaseModel):
    """
    https://core.telegram.org/bots/api#chatmembermember
    Represents a chat member that has no additional privileges
    or restrictions.
    """
    status: str
    user: User


class ChatMemberRestricted(BaseModel):
    """
    https://core.telegram.org/bots/api#chatmemberrestricted
    Represents a chat member that is under
     certain restrictions in the chat. Supergroups only.
    """
    status: str
    user: User
    is_member: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_send_messages: bool
    can_send_media_messages: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    until_date: datetime


class ChatMemberLeft(BaseModel):
    """
    https://core.telegram.org/bots/api#chatmemberleft
    Represents a chat member that isn't currently a member of the chat,
     but may join it themselves.
    """
    status: str
    user: User


class ChatMemberBanned(BaseModel):
    """
    https://core.telegram.org/bots/api#chatmemberbanned
    Represents a chat member
    that was banned in the chat and can't
    return to the chat or view chat messages.
    """
    status: str
    user: User
    until_date: int


class ChatInviteLink(BaseModel):
    """
    https://core.telegram.org/bots/api#chatinvitelink
    Represents an invite link for a chat.
    """
    invite_link: str
    creator: User
    is_primary: bool
    is_revoked: bool
    expire_date: Optional[int] = None
    member_limit: Optional[int] = None


class ChatMemberUpdated(BaseModel):
    """
    https://core.telegram.org/bots/api#chatmemberupdated
    This object represents changes in the status of a chat member.
    """
    chat: Chat
    from_user: User = Field(alias='from')
    date: datetime
    old_chat_member: Union[
        ChatMemberOwner, ChatMemberAdministrator,
        ChatMemberMember, ChatMemberRestricted,
        ChatMemberLeft, ChatMemberBanned]
    new_chat_member: Union[
        ChatMemberOwner, ChatMemberAdministrator,
        ChatMemberMember, ChatMemberRestricted,
        ChatMemberLeft, ChatMemberBanned]
    invite_link: Optional[ChatInviteLink]


class Update(BaseModel):
    """
    https://core.telegram.org/bots/api#update
    This object represents an incoming update.
At most one of the optional parameters can be present in any given update.
    """
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    inline_query: Optional[InlineQuery] = None
    chosen_inline_result: Optional[ChosenInlineResult] = None
    callback_query: Optional[CallbackQuery] = None
    shipping_query: Optional[ShippingQuery] = None
    pre_checkout_query: Optional[PreCheckoutQuery] = None
    poll: Optional[Poll] = None
    poll_answer: Optional[PollAnswer] = None
    my_chat_member: Optional[ChatMemberUpdated] = None
    chat_member: Optional[ChatMemberUpdated] = None


class WebhookInfo(BaseModel):
    """
    Contains information about the current status of a webhook.
    """

    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: Optional[str] = None
    last_error_date: Optional[datetime] = None
    last_error_message: Optional[str] = None
    max_connections: Optional[int] = None
    allowed_updates: Union[list, str, None] = None


# The following license applies to this file.

#                                  Apache License
#                            Version 2.0, January 2004
#                         http://www.apache.org/licenses/

#    TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

#    1. Definitions.

#       "License" shall mean the terms and conditions for use, reproduction,
#       and distribution as defined by Sections 1 through 9 of this document.

#       "Licensor" shall mean the copyright owner or entity authorized by
#       the copyright owner that is granting the License.

#       "Legal Entity" shall mean the union of the acting entity and all
#       other entities that control, are controlled by, or are under common
#       control with that entity. For the purposes of this definition,
#       "control" means (i) the power, direct or indirect, to cause the
#       direction or management of such entity, whether by contract or
#       otherwise, or (ii) ownership of fifty percent (50%) or more of the
#       outstanding shares, or (iii) beneficial ownership of such entity.

#       "You" (or "Your") shall mean an individual or Legal Entity
#       exercising permissions granted by this License.

#       "Source" form shall mean the preferred form for making modifications,
#       including but not limited to software source code, documentation
#       source, and configuration files.

#       "Object" form shall mean any form resulting from mechanical
#       transformation or translation of a Source form, including but
#       not limited to compiled object code, generated documentation,
#       and conversions to other media types.

#       "Work" shall mean the work of authorship, whether in Source or
#       Object form, made available under the License, as indicated by a
#       copyright notice that is included in or attached to the work
#       (an example is provided in the Appendix below).

#       "Derivative Works" shall mean any work, whether in Source or Object
#       form, that is based on (or derived from) the Work and for which the
#       editorial revisions, annotations, elaborations, or other modifications
#       represent, as a whole, an original work of authorship. For the purposes
#       of this License, Derivative Works shall not include works that remain
#       separable from, or merely link (or bind by name) to the interfaces of,
#       the Work and Derivative Works thereof.

#       "Contribution" shall mean any work of authorship, including
#       the original version of the Work and any modifications or additions
#       to that Work or Derivative Works thereof, that is intentionally
#       submitted to Licensor for inclusion in the Work by the copyright owner
#       or by an individual or Legal Entity authorized to submit on behalf of
#       the copyright owner. For the purposes of this definition, "submitted"
#       means any form of electronic, verbal, or written communication sent
#       to the Licensor or its representatives, including but not limited to
#       communication on electronic mailing lists, source code control systems,
#       and issue tracking systems that are managed by, or on behalf of, the
#       Licensor for the purpose of discussing and improving the Work, but
#       excluding communication that is conspicuously marked or otherwise
#       designated in writing by the copyright owner as "Not a Contribution."

#       "Contributor" shall mean Licensor and any individual or Legal Entity
#       on behalf of whom a Contribution has been received by Licensor and
#       subsequently incorporated within the Work.

#    2. Grant of Copyright License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       copyright license to reproduce, prepare Derivative Works of,
#       publicly display, publicly perform, sublicense, and distribute the
#       Work and such Derivative Works in Source or Object form.

#    3. Grant of Patent License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       (except as stated in this section) patent license to make, have made,
#       use, offer to sell, sell, import, and otherwise transfer the Work,
#       where such license applies only to those patent claims licensable
#       by such Contributor that are necessarily infringed by their
#       Contribution(s) alone or by combination of their Contribution(s)
#       with the Work to which such Contribution(s) was submitted. If You
#       institute patent litigation against any entity (including a
#       cross-claim or counterclaim in a lawsuit) alleging that the Work
#       or a Contribution incorporated within the Work constitutes direct
#       or contributory patent infringement, then any patent licenses
#       granted to You under this License for that Work shall terminate
#       as of the date such litigation is filed.

#    4. Redistribution. You may reproduce and distribute copies of the
#       Work or Derivative Works thereof in any medium, with or without
#       modifications, and in Source or Object form, provided that You
#       meet the following conditions:

#       (a) You must give any other recipients of the Work or
#           Derivative Works a copy of this License; and

#       (b) You must cause any modified files to carry prominent notices
#           stating that You changed the files; and

#       (c) You must retain, in the Source form of any Derivative Works
#           that You distribute, all copyright, patent, trademark, and
#           attribution notices from the Source form of the Work,
#           excluding those notices that do not pertain to any part of
#           the Derivative Works; and

#       (d) If the Work includes a "NOTICE" text file as part of its
#           distribution, then any Derivative Works that You distribute must
#           include a readable copy of the attribution notices contained
#           within such NOTICE file, excluding those notices that do not
#           pertain to any part of the Derivative Works, in at least one
#           of the following places: within a NOTICE text file distributed
#           as part of the Derivative Works; within the Source form or
#           documentation, if provided along with the Derivative Works; or,
#           within a display generated by the Derivative Works, if and
#           wherever such third-party notices normally appear. The contents
#           of the NOTICE file are for informational purposes only and
#           do not modify the License. You may add Your own attribution
#           notices within Derivative Works that You distribute, alongside
#           or as an addendum to the NOTICE text from the Work, provided
#           that such additional attribution notices cannot be construed
#           as modifying the License.

#       You may add Your own copyright statement to Your modifications and
#       may provide additional or different license terms and conditions
#       for use, reproduction, or distribution of Your modifications, or
#       for any such Derivative Works as a whole, provided Your use,
#       reproduction, and distribution of the Work otherwise complies with
#       the conditions stated in this License.

#    5. Submission of Contributions. Unless You explicitly state otherwise,
#       any Contribution intentionally submitted for inclusion in the Work
#       by You to the Licensor shall be under the terms and conditions of
#       this License, without any additional terms or conditions.
#       Notwithstanding the above, nothing herein shall supersede or modify
#       the terms of any separate license agreement you may have executed
#       with Licensor regarding such Contributions.

#    6. Trademarks. This License does not grant permission to use the trade
#       names, trademarks, service marks, or product names of the Licensor,
#       except as required for reasonable and customary use in describing the
#       origin of the Work and reproducing the content of the NOTICE file.

#    7. Disclaimer of Warranty. Unless required by applicable law or
#       agreed to in writing, Licensor provides the Work (and each
#       Contributor provides its Contributions) on an "AS IS" BASIS,
#       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#       implied, including, without limitation, any warranties or conditions
#       of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
#       PARTICULAR PURPOSE. You are solely responsible for determining the
#       appropriateness of using or redistributing the Work and assume any
#       risks associated with Your exercise of permissions under this License.

#    8. Limitation of Liability. In no event and under no legal theory,
#       whether in tort (including negligence), contract, or otherwise,
#       unless required by applicable law (such as deliberate and grossly
#       negligent acts) or agreed to in writing, shall any Contributor be
#       liable to You for damages, including any direct, indirect, special,
#       incidental, or consequential damages of any character arising as a
#       result of this License or out of the use or inability to use the
#       Work (including but not limited to damages for loss of goodwill,
#       work stoppage, computer failure or malfunction, or any and all
#       other commercial damages or losses), even if such Contributor
#       has been advised of the possibility of such damages.

#    9. Accepting Warranty or Additional Liability. While redistributing
#       the Work or Derivative Works thereof, You may choose to offer,
#       and charge a fee for, acceptance of support, warranty, indemnity,
#       or other liability obligations and/or rights consistent with this
#       License. However, in accepting such obligations, You may act only
#       on Your own behalf and on Your sole responsibility, not on behalf
#       of any other Contributor, and only if You agree to indemnify,
#       defend, and hold each Contributor harmless for any liability
#       incurred by, or claims asserted against, such Contributor by reason
#       of your accepting any such warranty or additional liability.

#    END OF TERMS AND CONDITIONS

#    APPENDIX: How to apply the Apache License to your work.

#       To apply the Apache License to your work, attach the following
#       boilerplate notice, with the fields enclosed by brackets "[]"
#       replaced with your own identifying information. (Don't include
#       the brackets!)  The text should be enclosed in the appropriate
#       comment syntax for the file format. We also recommend that a
#       file or class name and description of purpose be included on the
#       same "printed page" as the copyright notice for easier
#       identification within third-party archives.

#    Copyright 2022-2024 Dzmitry Drazdou

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.