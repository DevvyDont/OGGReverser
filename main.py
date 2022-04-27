from pydub import AudioSegment
import audioop
import wave
import shutil
import glob
import os


def reverse_wav(target_wav):

    with wave.open(target_wav) as fd:
        params = fd.getparams()
        frames = fd.readframes(1000000)  # 1 million frames max

    frames = audioop.reverse(frames, params.sampwidth)

    with wave.open(target_wav, 'wb') as fd:
        fd.setparams(params)
        fd.writeframes(frames)


def convert_to_wav(src, dst):
    # convert ogg to wav
    sound = AudioSegment.from_ogg(src)
    sound.export(dst, format="wav")


def convert_to_ogg(src, dst):
    # convert wav to ogg
    sound = AudioSegment.from_wav(src)
    sound.export(dst, format="ogg")


def main():
    target_dir = 'target'
    output_dir = 'output'

    print('Clearing the output directory')

    # Clear the output directory
    if 'output' in os.listdir():
        shutil.rmtree('output')

    print('Scanning which files to process')

    # Figure out which files we are going to convert by analyzing the target directory
    target_files = []
    for f in glob.glob(f'{target_dir}/**', recursive=True):
        # If it ends in ogg, we are going to process it
        if f.endswith('.ogg'):
            target_files.append(f)

    print(f"Found {len(target_files)} ogg files to reverse")

    # Copy all the files we want to work on to output
    copied_oggs = []
    for f in target_files:
        dst = f"{output_dir}/{f}"
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(f, dst)
        copied_oggs.append(dst)

    print(f"Succecssfully copied all ogg files to output for processing")

    # Loop through all the oggs copied in the output directory, convert them to wavs so we can reverse them
    for f in copied_oggs:
        convert_to_wav(f, f)

    print(f"Successfully converted all ogg files to wav files")

    # Once again, loop through all the wavs and reverse them
    for f in copied_oggs:
        reverse_wav(f)

    print(f"Successfully reversed all wav files")

    # Now, convert all the wavs back to oggs
    for f in copied_oggs:
        convert_to_ogg(f, f)

    print(f"Successfully converted all reversed wav files back to ogg files")
    print(f"Done! Processed {len(copied_oggs)} files")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
