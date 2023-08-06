import math
from .generalDistribution import Distribution
from matplotlib import pyplot as plt

class Gaussian(Distribution):
    """
    Gaussian distribution class for calculating and visualizing a Gaussian distribution.

    Attributes:
        mean(float): the mean value of the distribution termed as sigma
        stdev (float): representing the standard deviation of the distribution termed as mu
        data_list (list of floats): a list of floats extracted from the data file
    """
    def __init__(self, mu = 0, sigma = 1):
        Distribution.__init__(self, mu, sigma)

    def __add__(self, other):
        """
        Function to add together two Gaussian distributions

        Args:
            other (Gaussian): Gaussian Instance

        Returns:
            Gaussian: Gaussian Distribution
        """
        result = Gaussian()
        result.mean = self.mean + other.mean
        result.stdev = math.sqrt(self.stdev**2 + other.stdev**2)

    def __repr__(self):
        """
        Function to output the characteristics of the gaussian instance

        Args:
            None

        Returns:
            string: characteristics of the gaussian
        """
        return 'mean {}, standard deviation {}'.format(self.mean, self.stdev)

    def calculate_mean(self):
        """
        Function to calculate the mean of the data set

        Args:
            None

        Returns:
            float: mean of the data set
        """
        avg = 1.0*sum(self.data)/len(self.data)
        self.mean = avg
        return self.mean

    def calculate_stdev(self, sample=True):
        """
        Function to calculate the standard deviation of the data set

        Args:
            sample (bool): whether the data represents a sample or population

        Returns:
            float: satandard deviation of the data set
        """
        if sample:
            n = len(self.data) - 1
        else:
            n = len(self.data)
        mean = self.mean
        sigma = 0
        for d in self.data:
            sigma += (d - mean)**2
        sigma = math.sqrt(sigma / n)
        self.stdev = sigma
        return self.stdev

    def plot_histogram(self):
        """
        Function to output a histogram of the instance for the guassian distribution

        Args:
            None

        Returns:
            None
        """
        plt.hist(self.data, 20)
        plt.title("Histogram of data")
        plt.xlabel('data')
        plt.ylabel('count')
        plt.show()

    def pdf(self, x):
        """
        probability density function calculator for the gaussian distribution

        Args:
            x (float): point for calculating the probability density function

        Returns:
            float: probability density function output
        """
        self.calculate_mean()
        self.calculate_stdev() 
        return (1.0/ (self.stdev*math.sqrt(2*math.pi)) * math.exp((-0.5*((x - self.mean)/self.stdev)**2)))

    def plot_histogram_pdf(self, n_spaces = 100):
        """
        Function to plot the normalized histogram of the data and a plot of the probability density function along the same range

        Args:
            n_spaces (int): number of data points to plot

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
        """
        min_range = min(self.data)
        max_range = max(self.data)

        # calculate the interval between the x values
        interval = 1.0 * (max_range - min_range) / n_spaces

        x = []
        y = []

        # calculate the x values to visualize:
        for i in range(n_spaces):
            tmp = min_range + interval*i
            x.append(tmp)
            y.append(self.pdf(tmp))
        
        # plot the histogram
        fig, axes = plt.subplots(2, sharex=True)
        fig.subplots_adjust(hspace=0.6)
        axes[0].hist(self.data, 20, density=True)
        axes[0].set_title('Normal Histogram of data')
        axes[0].set_ylabel('Density')
        # plot the probability density function
        axes[1].plot(x, y)
        axes[1].set_title('Normal Distribution for \n sample Mean and Sample Standard Deviation')
        axes[1].set_ylabel('Density')
        plt.show()

        return x, y