import math
from .generalDistribution import Distribution
from matplotlib import pyplot as plt

class Binomial(Distribution):
    """
    Binomial distribution class for calculating and visualizing a Binomial distribution.

    Attributes:
        mean (float): representing the mean value of the distribution
        stdev (float): representing the standard deviation of the distribution
        data_list (list of floats): a list of floats to be extracted from the data file
        p (float): representing the probability of an event occurring
    """
    def __init__(self, mu=0, sigma=1):
        Distribution.__init__(self, mu, sigma)
        self.p = 0

    def __add__(self, other):
        """
        Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution  
        """
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise
        self.n = self.n + other.n
    
    def __repr__(self):
        """
        Function to output the characteristics of the binomial instance

        Args:
            None
        Returns:
            string: characteristics of the binomial
        """
        return 'mean {}, standard deviation {}, p {}, n {}'.format(self.mean, self.stdev, self.p, self.n)
        
    def replace_stats_with_data(self):
        """
        Function to calculate p and n from the data set. The function updates the p and n variables of the object.
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
        """
        self.n  = len(self.data)
        self.p = self.data.count(1)
        self.p = (self.p*1.0)/self.n
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        return self.mean, self.stdev

    def calculate_mean(self):
        """
        Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
        """
        self.mean = self.n*self.p
        return self.mean

    def calculate_stdev(self):
        """
        Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
        """
        self.stdev = math.sqrt(self.mean*(1 - self.p))

    def plot_bar(self):
        """
        Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
        plt.hist(self.data, 2)
        plt.title("Histogram of data")
        plt.xlabel('outcome')
        plt.ylabel('count')
        plt.show()

    def factorial(self, value):
        if value <= 1:
            return 1
        else:
            return value*self.factorial(value-1)

    def pdf(self, k=0):
        """
        Probability density function calculator for the binomial distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        Returns:
            float: probability density function output
        """
        self.replace_stats_with_data()
        nCk = (self.factorial(self.n)/(self.factorial(k)*self.factorial(self.n - k)))
        return nCk*(self.p**k)*((1-self.p)**(self.n - k))

    def plot_histogram_pdf(self):
        """
        Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot   
        """
        self.replace_stats_with_data()
        num = 0

        x = []
        y = []

        while num <= self.n:
            tmp = self.pdf(num)
            x.append(num)
            y.append(tmp)
            num += 1
        
        # plot the histogram
        fig, axes = plt.subplots(2, sharex=True)
        fig.subplots_adjust(hspace=0.6)
        axes[0].hist(self.data, 2, density=True)
        axes[0].set_title('Binomial Histogram of data')
        axes[0].set_ylabel('Count')
        # plot the probability density function
        axes[1].plot(x, y)
        axes[1].set_title('Binomial Distribution for \n Data')
        axes[1].set_ylabel('Density')
        plt.show()

        return x, y

