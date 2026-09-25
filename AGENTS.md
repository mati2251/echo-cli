# Echo CLI

## Project goal

Echo CLI is a small Python command-line utility for pronunciation practice. It should:

- listen to audio from the microphone,
- detect silence to determine when the user has finished speaking,
- play back the most recently recorded segment.

Keep the project focused on these features.

## Working guidelines

- The CLI should be very minimal (no additional arguments or commands are needed for now).
- It should have a way to communicate to the user when it is listening, recording, or playing back audio.
- Organize the code into small, easy-to-understand parts.
- Provide helpful errors when a microphone or playback device is unavailable, or when recording fails.
- Allow the silence duration and audio threshold to be configured as the project develops.

## Project status

Python is the chosen language. Audio libraries and implementation details are still to be decided.
