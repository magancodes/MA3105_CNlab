import random
import time

def simulate_go_back_n(total_frames, window_size, loss_probability):
    print("Go-Back-N ARQ Simulation")
    N = window_size
    base = 0
    next_seq_num = 0
    frames_sent = []
    
    while base < total_frames:
        # Sender: Send frames in the window
        while next_seq_num < base + N and next_seq_num < total_frames:
            frames_sent.append(next_seq_num)
            print(f"Sending frame {next_seq_num}", end=' ')
            next_seq_num += 1
        print()

        # Simulate transmission and loss
        lost_frame = -1
        for seq in frames_sent[base - len(frames_sent):]:
            if random.random() < loss_probability and lost_frame == -1:
                lost_frame = seq
                print(f"Frame {lost_frame} lost")
                break
        
        if lost_frame != -1:
            print(f"Frame {lost_frame} lost, retransmitting frames {lost_frame} {next_seq_num-1}")
            next_seq_num = lost_frame # Go Back N

        # Simulate ACK reception
        ack_received = base + N - 1 if lost_frame == -1 else base - 1
        if ack_received >= base and ack_received < total_frames:
            print(f"ACK {ack_received} received")
            base = ack_received + 1
            print(f"Window slides to {base} {base + N - 1}")
        
        time.sleep(0.2)

    print("\n--- Simulation Summary ---")
    print(f"Total Frames Delivered: {base}")

if __name__ == "__main__":
    TOTAL_FRAMES = 10
    WINDOW_SIZE = 4
    LOSS_PROB = 0.2
    simulate_go_back_n(TOTAL_FRAMES, WINDOW_SIZE, LOSS_PROB)
