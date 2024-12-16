import kafe2
import scipy.stats as stats

N_SIGMA_PEAK = 1

def pdf_signal(x, mu, sigma, a, b):
    return stats.norm.pdf(x, mu, sigma) / (stats.norm.cdf(b, mu, sigma) - stats.norm.cdf(a, mu, sigma))

def pdf_background(x, a, b):
    return 1/(b-a) 

def pdf_combined(x, mu, sigma, a, b, r):
    return r*pdf_signal(x, mu, sigma, a, b) + (1-r)*pdf_background(x, a, b)


def coincidenceFitter(data, a, b, peak_1, peak_2, mu_range=None, sigma_limit=None):
    # filter data
    peak1_lower = peak_1[0]-N_SIGMA_PEAK*peak_1[1]
    peak1_upper = peak_1[0]+N_SIGMA_PEAK*peak_1[1]
    mask1 = (data['height_1'] > peak1_lower) & (data['height_1'] < peak1_upper)
    
    peak2_lower = peak_2[0]-N_SIGMA_PEAK*peak_2[1]
    peak2_upper = peak_2[0]+N_SIGMA_PEAK*peak_2[1]
    mask2 = (data['height_2'] > peak2_lower) & (data['height_2'] < peak2_upper)
    
    time_differences = data[mask1 & mask2]['time_difference']
    
    bin_edges = np.arange(a,b)
    container = kafe2.HistContainer(bin_edges = bin_edges, fill_data = time_differences)
    
    # fit H0 i.e. background only r=0
    
    
    
    
    
    
    
    
    