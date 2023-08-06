class Distribution():
    """
    Gaussian distribution class for calculating and visualizing a Gaussian distribution.

    Attributes:
        mean(float): the mean value of the distribution termed as sigma
        stdev (float): representing the standard deviation of the distribution termed as mu
        data_list (list of floats): a list of floats extracted from the data file
    """
    def __init__(self, mu = 0, sigma = 1):
        self.mean = mu
        self.stdev = sigma
        self.data = []

    def read_data_file(self, file_name):
        """
        Function to read in data file from a text file, The text file should have one number (float)
        per line, The numbers are stored in the data attribute. After reading in the data file, the mean and standard deviation 
        are calculated

        Args:
            file_name (string):  name of a file to read data from

        Returns:
            None
        """
        with open(file_name) as file:
            data_list = []
            line = file.readline()
            while line: #This makes sure that it stores a line if it holds an integer value
                data_list.append(int(line))
                line = file.readline()    
        file.close()
        self.data = data_list