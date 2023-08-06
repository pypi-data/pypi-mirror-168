import requests
import json
from requests.exceptions import ConnectionError
from .exceptions import InvalidArgumentError, BadRequestError, UnauthorizedError, InternalServerError, \
    check_response_status


class FaceAuth:
    """
    Instantiate a face authentication process.

    :param api_key: API key.
    :type api_key: str
    """

    def __init__(self, api_key):
        """
        Initialize a `FaceAuth` object.

        :param api_key: API key.
        :type api_key: str
        """
        self.api_key = api_key

    def authenticate(self,
                     image_file,
                     video_file,
                     accuracy='normal',
                     face_detection_model="default",
                     face_recognition_model="default",
                     detect_face_spoofing=False
                     ):
        """
        Returns face authentication result given a picture and a video of user's face using API.

        :param image_file: An image of user's face.
        :type image_file: str
        :param video_file: A video of user's face, maximum 60 seconds.
        :type video_file: str
        :param accuracy: The preferred accuracy chosen from ['strict', 'normal', 'lenient']; Default is 'normal'.
        :type accuracy: str
        :param face_detection_model: The preferred 'face detection model' from chosen from ['default', 'mobile',
        'light']; Default is 'default'.
        :type face_detection_model: str
        :param face_recognition_model: The preferred 'face recognition model' chosen from ['default', 'mobile'];
        Default is 'default'.
        :type face_recognition_model: str
        :param detect_face_spoofing: Whether to perform 'face spoofing detection' or not.
        :type detect_face_spoofing: bool

        :return: Authentication result; `True` or `False`
        :rtype: bool
        """

        if not image_file:
            raise InvalidArgumentError("Pythonlib Error: No input image_file provided.")

        if not video_file:
            raise InvalidArgumentError("Pythonlib Error: No input video_file provided.")

        if accuracy not in ['strict', 'normal', 'lenient']:
            raise InvalidArgumentError("Pythonlib Error: accuracy value should be chosen from ['strict', 'normal', "
                                       "'lenient'].")

        if detect_face_spoofing and type(detect_face_spoofing) is not bool:
            raise InvalidArgumentError("Pythonlib Error: Invalid detect_face_spoofing value (should be True or False).")

        auth_result = False

        url = f'https://py-face-api-2.agiagents.com/authenticate'

        params = {
            'face_detection_model': face_detection_model,
            'face_recognition_model': face_recognition_model,
            'detect_face_spoofing': detect_face_spoofing,
            'api_key': self.api_key,
        }

        files = {
           "image_file": open(image_file, 'rb'),
           "video_file": open(video_file, 'rb')
        }

        try:
            raw_response = requests.post(url, params=params, files=files)
            check_response_status(raw_response)
            response = raw_response.json()
            if response.get('similarity'):

                if accuracy is 'normal':
                    auth_result = response['similarity'] > 0.69

                elif accuracy is 'lenient':
                    auth_result = response['similarity'] > 0.60

                elif accuracy is 'strict':
                    auth_result = response['similarity'] > 0.75

            else:
                raise InternalServerError('Pythonlib Error: Error getting similarity from response. Contact your '
                                          'product owner for an update if you are sure the query is right.')

        except ConnectionError as exception:
            raise ConnectionError('Pythonlib Error: There is a problem with network connection.', exception.args) \
                from exception

        except json.JSONDecodeError as jsonDecodeError:
            raise InternalServerError('Pythonlib Error: Error parsing the response to JSON. Contact your product '
                                      'owner for an update if you are sure the query is right.') from jsonDecodeError

        except BadRequestError as exception:
            raise BadRequestError('Pythonlib Error. ' + exception.args[0])

        except UnauthorizedError as exception:
            raise UnauthorizedError('Pythonlib Error. ' + exception.args[0])

        except InternalServerError as exception:
            raise InternalServerError('Pythonlib Error. ' + exception.args[0])

        except Exception as exception:
            raise exception.__class__('Pythonlib Error. ', exception.args) from exception

        finally:
            files['image_file'].close()
            files['video_file'].close()

        return auth_result
