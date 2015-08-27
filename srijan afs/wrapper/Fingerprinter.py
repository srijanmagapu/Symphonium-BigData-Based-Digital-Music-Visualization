"""Class doc"""

import math
import wave
import numpy
from warnings import warn

#Author - Srijan Magapu - Symphonium Project

class Fingerprinter(object):
    """

    """
    
    # constants
    FREQUENCY_BAND_LOWER_LIMIT = 300.0  # only frequencies (in Hz) in this band are analysed
    FREQUENCY_BAND_UPPER_LIMIT = 2000.0 #
    FINGERPRINT_NBITS = 32              # number of bits for the fingerprint of a frame
    
    # raw properties (given by the user)
    wavefile = None                
    framewidth = None              
    overlap = None                 
    
    # derived properties
    nsamples = None                
    nsamples_per_frame = None
    nframes = None                 
    samples_rate = None            
    sample_width = None            
    resolution = None              
    nsamples_between_frames = None 
    frequency_band_boundary_indices = numpy.zeros(FINGERPRINT_NBITS) # Boundaries of the frequency bands used for fingerprint generation

    index_width_lower_to_upper = None # how many fourier components lie within 300Hz..2000Hz
    
    # arrays that contain all the sub-fingerprints of the wave file
    fingerprints = None
    fingerprints_binary = None
        def __init__(self, filepath=None, framewidth=0.37, overlap=31.0/32.0):
        self.wavefile = wave.open(filepath, 'rb')
        self.framewidth = framewidth
        self.overlap = overlap
        
        n_channels = self.wavefile.getnchannels()        
        self.sample_width = self.wavefile.getsampwidth()
        self.nsamples = self.wavefile.getnframes()       ]
        self.sample_rate = self.wavefile.getframerate()  # how many samples per second?

        length_in_seconds = self.nsamples / self.sample_rate # length of the whole track
        
        if (( n_channels > 1 ) or (self.sample_width != 2)):
            raise Exception("Can only work with 16bit mono wave files currently.")
        
        # Input validation
        # Frames must be smaller than the entire length of the file
        if ( self.framewidth > length_in_seconds or self.framewidth < 0.0):
            warn("Framewidth larger than entire audio file! Defaulting to the whole length.")
            self.framewidth = length_in_seconds
        # overlap must be between 0 and 1
        if ( self.overlap >= 1.0 or self.overlap < 0.0 ):
            warn("Overlap must be within [0, 1). Defaulting to 31/32.") 
            self.overlap = 31.0/32.0
            
        # calculate derived quantities
        self.nsamples_per_frame = math.floor(self.sample_rate * self.framewidth)
        self.resolution = (1.0 - self.overlap) * self.framewidth
        self.nsamples_between_frames = math.floor((1.0 - self.overlap) * self.nsamples_per_frame)
        if ( self.nsamples_between_frames == 0):
            self.nsamples_between_frames = 1 # advance at least one sample for each sub-fingerprint!
        self.nframes = math.floor( self.nsamples / self.nsamples_between_frames )
            
        # init array of sub-fingerprints, length is the number of frames
        self.fingerprints = numpy.zeros(self.nframes)
        self.fingerprints_binary = numpy.zeros((self.nframes, self.FINGERPRINT_NBITS), dtype=numpy.bool)
        
        # given the number of samples in a frame and its length in seconds, we can calculate
        # the indices that indicate the boundaries between frequency bands
        # we do this once at initialization
        self.frequency_band_boundary_indices = self.calculate_frequency_bands(self.nsamples_per_frame, self.framewidth)


    def close(self):
      self.wavefile.close()


    # actually calculate all sub-fingerprints
    def init_fingerprints(self):
        # read all bytes from wavefile
        data = numpy.frombuffer(self.wavefile.readframes(self.nsamples), dtype="i" + str(self.sample_width))
        
        # loop through the file, calculating the sub-fingerprint for each frame
        position = 0 + self.nsamples_between_frames
        there_are_frames_left = (position < (self.nsamples - self.nsamples_per_frame) )
        
        last_frame = data[0:self.nsamples_per_frame]
        fft_last_frame = numpy.fft.rfft(numpy.hamming(self.nsamples_per_frame) * last_frame)
        #fft_last_frame = numpy.fft.rfft( last_frame)
        index_fingerprint = 0
        
        powers = 2 ** numpy.arange(0, self.FINGERPRINT_NBITS)
        while there_are_frames_left:
            current_frame = data[position:position + self.nsamples_per_frame]
            # fourier transform current frame, weighted in time by hamming window
            fft_current_frame = numpy.fft.rfft(numpy.hamming(self.nsamples_per_frame) * current_frame)
            #fft_current_frame = numpy.fft.rfft(current_frame)
            
            # crunch crunch crunch
            self.fingerprints_binary[index_fingerprint] = self.generate_binary_fingerprint_from_frames(fft_last_frame, fft_current_frame)
            self.fingerprints[index_fingerprint] = numpy.sum(powers * self.fingerprints_binary[index_fingerprint])
            
            position = position + self.nsamples_between_frames
            there_are_frames_left = (position < (self.nsamples - self.nsamples_per_frame) )
            last_frame = current_frame
            fft_last_frame = fft_current_frame
            index_fingerprint = index_fingerprint + 1
            
            #print position
            #print current_frame.shape
            #print fft_current_frame.shape
            # this should print the index with the maximum pressure in this frame
            # index(frequency) =   length_of_interval_in_seconds * frequency
            #print numpy.argmax(fft_current_frame)
            #print current_frame
            #print "***"
            
            # Keep on going as long as there are enough samples left for a whole frame
        self.wavefile.close();
    
    
    
     
        
        index_lower_limit = int(math.floor( frame_length * self.FREQUENCY_BAND_LOWER_LIMIT )) # index of 300Hz freq component
        index_upper_limit = int(math.ceil( frame_length * self.FREQUENCY_BAND_UPPER_LIMIT )) # index of 2000Hz freq component
        index_width = index_upper_limit - index_lower_limit + 1 # how many entries lie within 300Hz..2000Hz
        self.index_width_lower_to_upper = index_width
        

        a = float(index_lower_limit)
        b = numpy.log( float(index_upper_limit)/a ) / float(self.FINGERPRINT_NBITS + 1)
        # return indices for the frequency bands
        return numpy.round( a * numpy.exp(b * numpy.arange(0,self.FINGERPRINT_NBITS + 2)) )
        
        
        
    def generate_binary_fingerprint_from_frames(self, frame1, frame2):
        """
        Generate a sub-fingerprint for a frame
        """
        fingerprint = numpy.zeros(self.FINGERPRINT_NBITS, dtype=numpy.bool)
        
        energies1 = self.calculate_band_energies_from_frame(frame1)
        energies2 = self.calculate_band_energies_from_frame(frame2)
        for band in range(self.FINGERPRINT_NBITS):
            fingerprint[band] = energies2[band] - energies2[band+1] > energies1[band] - energies1[band+1]
            
        return fingerprint
        #self.frequency_band_boundary_indices
      
      
      
    def calculate_band_energies_from_frame(self, frame):
        """
        Calculate the sum of fourier components of a frame, by bands
        """
        energies = numpy.zeros(self.FINGERPRINT_NBITS + 1)
        for band in range(self.FINGERPRINT_NBITS + 1):
            energies[band] = numpy.sum ( numpy.abs( frame[ self.frequency_band_boundary_indices[band] : self.frequency_band_boundary_indices[band+1]  ] ) ** 2 )
        return energies
    
    
    
    def binary_distance(self, print1, print2):
        return numpy.sum(numpy.logical_xor(print1, print2))
    
    
    
    def block_distance(self, block1, block2):
        if block1.shape != block2.shape:
            raise "You are trying to calculate the distance between two different objects."
        block_dist = 0
        for i in range(len(block1)):
            block_dist += self.binary_distance(block1[i], block2[i])
        return block_dist
        
        
         if block_length > 256:
            block_length = 256
        
        min = 10000000000
        index = 0
        for i in range(len(self.fingerprints) - block_length):
            diff = self.block_distance(compare[:block_length], self.fingerprints_binary[i:i+block_length])
            if diff < min:
                print "found new minimum at " + str(i) + " (" + str(float(i) * self.nsamples_between_frames / self.sample_rate) + ") - " + str(diff)
                index = i
                min = diff
                
        print float(index) * self.nsamples_between_frames / self.sample_rate
