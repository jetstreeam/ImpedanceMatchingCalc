#%%
import skrf as rf
import matplotlib.pyplot as plt

def plot_smith_chart(network):
    fig, ax = plt.subplots()
    ax.set_title('Smith Chart')

    # Plot the network on the Smith chart
    network.plot_s_smith(m=0, n=0, ax=ax, linestyle='-', color='b', label='Network',chart_type='zy')

    # Show the legend
    ax.legend()

    plt.show()

def main():
    # Create a sample network (you can replace this with your own S-parameter data)
    frequency = rf.Frequency(start=1, stop=10, npoints=101, unit='GHz')
    network = rf.Network(frequency=frequency, s=(0.5 + 0.5j) * rf.ones(101))

    # Plot the Smith chart
    plot_smith_chart(network)
    

if __name__ == "__main__":
    main()

    
