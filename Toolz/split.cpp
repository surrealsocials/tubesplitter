#include <iostream>
#include <string>
#include <C:\Projects\tubesplitter\Toolz\lame\include\lame.h>

void convert_wav_to_mp3(const std::string &wav_path, const std::string &mp3_path) {
    lame_global_flags *lame_flags = lame_init();
    if (!lame_flags) {
        std::cerr << "Error initializing LAME" << std::endl;
        return;
    }

    FILE *wav_file = fopen(wav_path.c_str(), "rb");
    FILE *mp3_file = fopen(mp3_path.c_str(), "wb");

    if (!wav_file || !mp3_file) {
        std::cerr << "Error opening files" << std::endl;
        return;
    }

    // Set LAME options
    lame_set_num_channels(lame_flags, 2);  // Stereo
    lame_set_in_samplerate(lame_flags, 44100);  // Sample rate
    lame_set_brate(lame_flags, 192);  // Bit rate (192 kbps)
    lame_set_quality(lame_flags, 2);  // Highest quality

    // Initialize LAME
    if (lame_init_params(lame_flags) < 0) {
        std::cerr << "Error initializing LAME parameters" << std::endl;
        return;
    }

    const int PCM_SIZE = 8192;
    short pcm_buffer[PCM_SIZE * 2];
    unsigned char mp3_buffer[PCM_SIZE * 2];

    while (true) {
        int read_size = fread(pcm_buffer, sizeof(short) * 2, PCM_SIZE, wav_file);
        if (read_size <= 0) {
            break;
        }

        int encoded_size = lame_encode_buffer_interleaved(lame_flags, pcm_buffer, read_size, mp3_buffer, PCM_SIZE * 2);
        if (encoded_size < 0) {
            std::cerr << "Error encoding audio" << std::endl;
            break;
        }

        fwrite(mp3_buffer, 1, encoded_size, mp3_file);
    }

    // Flush and finalize
    int remaining_bytes = lame_encode_flush(lame_flags, mp3_buffer, PCM_SIZE * 2);
    if (remaining_bytes > 0) {
        fwrite(mp3_buffer, 1, remaining_bytes, mp3_file);
    }

    lame_close(lame_flags);
    fclose(wav_file);
    fclose(mp3_file);

    std::cout << "MP3 conversion complete: " << mp3_path << std::endl;
}

void run(const std::string &title) {
    // Construct the command arguments
    std::string wav_path = "content/" + title + "/accompaniment.wav";
    std::string mp3_path = "content/" + title + "/accompaniment.mp3";
    
    convert_wav_to_mp3(wav_path, mp3_path);
    
    // Repeat the conversion for other stems (bass, drums, vocals) if needed
    
    std::cout << "All conversions complete for " << title << std::endl;
}

int main() {
    std::string target_title = "C:\\Projects\\tubesplitter\\content\\Camaron_de_la_isla_P\\Audio.mp3";  // Replace with the actual target title
    run(target_title);

    return 0;
}
