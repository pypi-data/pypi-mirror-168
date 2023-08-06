
## Write srcipt Plain text
def lines(fileName,lines):
    """ Funtion to write a list into text file.

    Args:
        file_name(str): file name.
        lines(list-of-str): list of strings.

    Returns:
        file   
    """
    with open(fileName,'w') as f:
        for line in lines:
            f.write( ''.join([line,'\n']) )

    print('Write TEXT file, done !')
    return

