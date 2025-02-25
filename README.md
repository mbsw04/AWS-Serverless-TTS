Text-to-Speech API (POST Request):

Input (Request Body):
When the client (frontend) sends a request to the Text-to-Speech API, the body of the POST request might look like this:

{
    "text": "Hello, welcome to our text-to-speech service.",
    "language": "en-US",
    "voice": "Joanna"
}

text: The text that you want to convert to speech. (In this case, "Hello, welcome to our text-to-speech service.")
language: The language in which the text should be spoken. (In this case, "en-US" for American English)
voice: The voice in which the text should be read. (In this case, "Joanna", which is a female voice in Amazon Polly)
Output (Response Body):
The Text-to-Speech API returns a JSON response with the URL to the generated audio file in S3 and the S3 object key for the file:

{
    "audioUrl": "https://your-bucket-name.s3.amazonaws.com/text-to-speech/abc123.mp3",
    "s3Key": "text-to-speech/abc123.mp3"
}

audioUrl: The public URL to the generated audio file stored in S3, which can be used to play or download the audio file.
s3Key: The unique identifier for the file in S3. This key is used to identify and delete the file later.


File Deletion API (POST Request):

Input (Request Body):
When the client sends a request to the File Deletion API, the body of the POST request will contain the s3Key of the file to be deleted:

{
    "s3Key": "text-to-speech/abc123.mp3"
}

s3Key: The S3 key of the file that needs to be deleted. This key is provided by the Text-to-Speech API in the earlier response.
Output (Response Body):
If the file is deleted successfully, the API returns a success message:

{
    "message": "File deleted successfully"
}