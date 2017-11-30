def filterBands(noiseFile='hyper_bands.csv', dataFile='hyper_bands_train.csv',
    output='hyper_bands_train_no_noise.csv'):
    '''
    Creates file named @output, a copy of file named @dataFile, which doesn't 
    contain the columns (hyperspectral band intensity)that are too noisy to be 
    valid, as indicated in file named @noiseFile.
    '''
    NOISE_COLUMN_INDEX = -1
    BAND_NUM_INDEX = 0
    badData = []
    badColumns = []
    newHeaders = []
    with open(noiseFile, 'r') as inFile:
        inFile.readline()
        for line in inFile:
            data = line.rstrip().split(',')
            if int(data[NOISE_COLUMN_INDEX]):
                badData.append(data[BAND_NUM_INDEX])
    with open(dataFile, 'r') as inFile:
        with open(output, 'w') as outFile:
            headers = inFile.readline().rstrip('\n').split(',')
            for i in range(len(headers)):
                if headers[i] in badData:
                    badColumns.append(i)
                else:
                    newHeaders.append(headers[i])
            outFile.write(','.join(newHeaders) + '\n')
            for line in inFile:
                newLine = []
                data = line.rstrip('\n').split(',')
                for i in range(len(data)):
                    if i not in badColumns:
                        newLine.append(data[i])
                outFile.write(','.join(newLine) + '\n')


def condenseCrownData(dataFile='hyper_bands_train_no_noise.csv',
    output='hyper_bands_train_reformatted.csv'):
    '''
    Creates file named @output, a copy of file named @dataFile which averages 
    all values of each column (chm or hyperspectral band intensity) for each 
    unique crown id (averages values of all pixels belonging to crown). 
    '''
    crownData = {}
    averages = []
    with open(dataFile, 'r') as inFile:
        with open(output, 'w') as outFile:
            headers = inFile.readline().rstrip('\n').split(',')
            numColumns = len(headers) - 1
            outFile.write(','.join(headers) + '\n')
            for line in inFile:
                data = line.rstrip().split(',')
                crownData.setdefault(data[0], []).append(data[1:])
            for crown in crownData.keys():
                averages = []
                for i in range(numColumns):
                    averages.append([])
                for pixel in crownData[crown]:
                    for i in range(len(pixel)):
                        averages[i].append(float(pixel[i]))
                newLine = [crown]
                for i in range(len(averages)):
                    newLine.append(
                        str(sum(averages[i]) / float(len(averages[i]))))
                outFile.write(','.join(newLine) + '\n')


filterBands()
condenseCrownData()
