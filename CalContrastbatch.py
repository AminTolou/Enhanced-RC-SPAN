import torch  

def CalContrastbatch(Input):  
    # Ensure that the input is on the GPU  
    Input = Input.cuda()  
    
    # Get the input shape (batch_size, channels, height, width)  
    batch_size, c, h, w = Input.shape  
    
    # Check if the input shape is correct  
    #assert batch_size == 1 and c == 64 and h == 192 and w == 192, "Input must be of shape (1, 64, 192, 192)"  
    
    # Initialize a tensor for the contrast results  
    Contrast = torch.zeros(batch_size, c, 1, 1).cuda()  # Size (1, 64, 1, 1)  

    # Calculate standard deviation over the height and width dimensions (2 and 3)  
    Contrast[:, :, 0, 0] = torch.std(Input, dim=[2, 3], unbiased=True)  

    return Contrast 