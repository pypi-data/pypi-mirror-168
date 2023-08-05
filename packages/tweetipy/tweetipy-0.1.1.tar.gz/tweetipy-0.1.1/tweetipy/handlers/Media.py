from typing import Literal
from tweetipy.helpers.API import API_OAUTH_1_0_a

_MediaType = Literal[ # The MIME type of the media being uploaded.
        "video/mp4",
        "image/jpeg",
        "image/png",
        "image/gif"
    ]

class _MediaUpload_INIT_Response():
        def __init__(self, media_id: int, media_id_string: str, expires_after_secs: int) -> None:
            self.media_id = media_id
            self.media_id_string = media_id_string
            self.expires_after_secs = expires_after_secs

class _MediaUpload_processing_info():
    def __init__(self, state: str, check_after_secs: int) -> None:
        self.state = state
        self.check_after_secs = check_after_secs
        # check after x seconds for update using STATUS command

class _MediaUpload_image_info():
    def __init__(self, image_type: _MediaType, w: int, h: int) -> None:
        self.image_type = image_type
        self.w = w
        self.h = h

class _MediaUpload_video_info():
    def __init__(self, video_type: _MediaType) -> None:
        self.video_type = video_type

class _MediaUpload_FINALIZE_Response():
        def __init__(self, media_id: int, media_id_string: str, expires_after_secs: int, size: int, processing_info: _MediaUpload_processing_info = None, image: _MediaUpload_image_info = None, video: _MediaUpload_video_info = None) -> None:
            self.media_id = media_id
            self.media_id_string = media_id_string
            self.expires_after_secs = expires_after_secs
            self.size = size
            self.processing_info = processing_info

class HandlerMedia():

    def __init__(self, API: API_OAUTH_1_0_a) -> None:
        self.API = API
    
    def _chunk_upload_INIT(self, media_type: _MediaType, total_bytes: int, media_category: str = None, additional_owners: str = None) -> _MediaUpload_INIT_Response:
        """
        Returns a json object containing media_id, media_id_string and
        expires_after_secs. See example response:
        {
            "media_id": 601413451156586496,
            "media_id_string": "601413451156586496",
            "expires_after_secs": 3599
        }
        """
        endpoint = 'https://upload.twitter.com/1.1/media/upload.json'
        params = {
            "command": "INIT",
            "media_type": media_type,
            "total_bytes": total_bytes
        }
        if media_category != None:
            # A string enum value which identifies a media usecase. This
            # identifier is used to enforce usecase specific constraints (e.g.
            # file size, video duration) and enable advanced features. 	
            params["media_category"] = media_category
        if additional_owners != None:
            # A comma-separated list of user IDs to set as additional owners
            # allowed to use the returned media_id in Tweets or Cards. Up to 100
            # additional owners may be specified.
            params["additional_owners"] = additional_owners
        
        r = self.API.post(
            endpoint,
            params=params
        )
        try:
            print(r.status_code)
            return _MediaUpload_INIT_Response(**r.json())
        except:
            r.raise_for_status()
    
    def _chunk_upload_APPEND(self, media_id: str, segment_index: int, media_bytes: bytes = None, media_data: bytes = None) -> bool:
        """
        HTTP 2XX will be returned with an empty response body on successful
        upload.
        """
        if (media_bytes != None) + (media_data != None) != 1:
            raise Exception("You must provide one (and only one) of media_bytes or media_data.")
        
        endpoint = 'https://upload.twitter.com/1.1/media/upload.json'
        
        params = {
            "command": "APPEND",
            "media_id": media_id,
            "segment_index": segment_index,
        }
        
        if media_bytes != None:
            files = {
                "media": media_bytes,
            }
        else:
            files = None
            params["media_data"] = media_data

        # file_field = filefield # Example: "media" ????
        r = self.API.post(url=endpoint, params=params, files=files)
        if str(r.status_code)[0] == "2":
            return True
        else:
            print(r.status_code)
            print(r.text)
            r.raise_for_status()
            # And, just in case r contains no errors, raise a custom exception:
            raise Exception(f"Error processing chunk {segment_index} of upload.")

    def _chunk_upload_FINALIZE(self, media_id: str) -> _MediaUpload_FINALIZE_Response:
        """
        Upon sucess, it return a media_id (and a media_id_str). Use the
        media_id_str where possible.

        The returned id is only valid for "expires_after_secs" seconds. Any
        attempt to use mediaId after this time period in other API calls will
        result in a Bad Request (HTTP 4xx) response.

        If the response contains a processing_info field, then use the STATUS
        command to poll for the status of the FINALIZE operation.
        If a processing_info field is NOT returned in the response, then
        media_id is ready for use in other API endpoints.

        Here is an example response:
        {
            "media_id": 601413451156586496,
            "media_id_string": "601413451156586496",
            "size": 4430752,
            "expires_after_secs": 3600,
            "video": {
                "video_type": "video/mp4"
            }
        }
        """
        endpoint = 'https://upload.twitter.com/1.1/media/upload.json'
        
        params = {
            "command": "FINALIZE",
            "media_id": media_id
        }

        r = self.API.post(url=endpoint, params=params)
        return _MediaUpload_FINALIZE_Response(**r.json())


    def upload(
        self,
        media_bytes: bytes,
        media_type: _MediaType,
        media_category: str = None,
        additional_owners: str = None
    ) -> _MediaUpload_FINALIZE_Response:
        """
        Returns media_id after successful upload.
        Uses Twitter v1 api because it is not implemented in v2 yet.
        For current state of Twitter's development, see:
        https://trello.com/c/Zr9zDrJx/109-replacement-of-media-uploads-functionality

        Size restrictions for uploading via API 

        * Image 5 MB
        * GIF 15 MB
        * Video 512 MB (when using media_category=amplify)

        """
        media_size = len(media_bytes)

        INIT = self._chunk_upload_INIT(
            media_type=media_type,
            total_bytes=media_size,
            media_category=media_category,
            additional_owners=additional_owners)

        chunk_size = 20_000 # bytes
        sent_chunks_count = 0
        sent_bytes_count = 0
        while sent_bytes_count < media_size:
            byte_from = sent_bytes_count
            byte_to = min(sent_bytes_count + chunk_size, media_size)
            self._chunk_upload_APPEND(
                media_id=INIT.media_id_string,
                segment_index=sent_chunks_count,
                media_bytes=media_bytes[byte_from:byte_to]
            )
            sent_bytes_count += (byte_to - byte_from)
            sent_chunks_count += 1

        FINALIZE = self._chunk_upload_FINALIZE(
            media_id=INIT.media_id_string
        )
        # print(FINALIZE.media_id)
        # print(FINALIZE.media_id_string)
        # print(FINALIZE.expires_after_secs)
        # if FINALIZE.processing_info != None:
        #     print(FINALIZE.processing_info.state)
        #     print(FINALIZE.processing_info.check_after_secs)
        # print(FINALIZE.size)
        return FINALIZE

        