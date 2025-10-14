import matplotlib.pyplot as plt

def simulate_tcp_congestion_control(threshold_init, total_rounds):
    print("TCP Congestion Control Simulation")
    cwnd = 1.0
    ssthresh = float(threshold_init)
    rounds = []
    cwnd_values = []
    
    for round_num in range(1, total_rounds + 1):
        rounds.append(round_num)
        cwnd_values.append(cwnd)
        
        
        if round_num == 7:
            print(f"Round {round_num}: Packet loss detected (Timeout/Triple Duplicate ACK).")
            # Timeout/Multiplicative Decrease
            ssthresh = max(cwnd / 2, 2.0)
            cwnd = 1.0
            print(f"New ssthresh: {ssthresh}, cwnd reset to {cwnd}")
            continue

      
        if cwnd < ssthresh:
            
            cwnd += 1
            print(f"Round {round_num}: Slow Start, cwnd={cwnd}, ssthresh={ssthresh}")
        
        else:
            cwnd += (1 / cwnd)
            print(f"Round {round_num}: Congestion Avoidance, cwnd={cwnd:.2f}, ssthresh={ssthresh}")

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(rounds, cwnd_values, marker='o', linestyle='-', color='b')
    plt.axhline(y=threshold_init, color='r', linestyle='--', label='Initial ssthresh')
    plt.title('TCP Congestion Window (cwnd) vs. Transmission Rounds')
    plt.xlabel('Transmission Rounds')
    plt.ylabel('Congestion Window (cwnd)')
    plt.grid(True)
    plt.legend()
    plt.savefig('cwnd_plot.png')
    print("\nPlot saved as cwnd_plot.png")

if __name__ == "__main__":
    SSTHRESH_INIT = 8
    TOTAL_ROUNDS = 15
    simulate_tcp_congestion_control(SSTHRESH_INIT, TOTAL_ROUNDS)
