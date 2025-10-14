import random
import time

def simulate_stop_and_wait(total_frames, loss_probability):
    print("Stop-and-Wait ARQ Simulation")
    next_frame_to_send = 0
    frames_sent = 0
    frames_retransmitted = 0
    total_delivered = 0

    while total_delivered < total_frames:
        frame_sent_time = time.time()
        print(f"Sending Frame {next_frame_to_send}")
        frames_sent += 1

        is_lost = random.random() < loss_probability

        if is_lost:
            print(f"Frame {next_frame_to_send} lost, retransmitting..")
            frames_retransmitted += 1
            # Simulate timeout and retransmission
            time.sleep(0.1)
            continue
        
        # Simulate ACK reception
        print(f"ACK {next_frame_to_send} received")
        total_delivered += 1
        next_frame_to_send = (next_frame_to_send + 1) % 2
        time.sleep(0.05)

    print("\n--- Simulation Summary ---")
    print(f"Total Frames to Deliver: {total_frames}")
    print(f"Total Frames Sent: {frames_sent}")
    print(f"Total Frames Acknowledged: {total_delivered}")
    print(f"Total Frames Retransmitted: {frames_retransmitted}")

if __name__ == "__main__":
    TOTAL_FRAMES = 5
    LOSS_PROB = 0.3
    simulate_stop_and_wait(TOTAL_FRAMES, LOSS_PROB)
