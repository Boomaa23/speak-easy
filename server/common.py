import ffmpeg


def mp3_to_pcm(mp3_bytes):
    ffmpeg_process = (
        ffmpeg
        .input('pipe:0')
        .output('pipe:1', format='f32le', acodec='pcm_f32le', ac=1, ar='32k')
        .run_async(pipe_stdin=True, pipe_stdout=True)
    )
    ffmpeg_process.stdin.write(mp3_bytes)

    out = []
    b = ffmpeg_process.stdout.read(1)
    while b:
        out.append(b)
    return out

