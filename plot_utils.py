import matplotlib.pyplot as plt

def plot_depth(depth_history):
    for cid, values in depth_history.items():
        plt.plot(values, label=f"Car {cid}")
    plt.xlabel("Frame")
    plt.ylabel("Relative Depth")
    plt.legend()
    plt.show()


def plot_gap(gap_history):
    for pair, values in gap_history.items():
        plt.plot(values, label=f"{pair}")
    plt.xlabel("Frame")
    plt.ylabel("Gap Proxy")
    plt.legend()
    plt.show()
