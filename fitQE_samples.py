import matplotlib.pyplot as plt
import fitQE_1sample

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('infileList',
                        nargs = '+',
                        type = str,
                        help = 'CSV data obtained with oscilloscope')
    parser.add_argument('--plot', '-p',
                        type = str,
                        help = '\'f\': Save fit result plot to Plots/ directory,\n \
                                \'s\': Show plot in window')
    args = parser.parse_args()

    QEs = []
    for infile in args.infileList:
        args.infile = infile
        args.plotfile = True
        args.verbose = False
        QE = fitQE_1sample.main(args)
        plt.close()
        print(infile,"processed. QE =",QE)
        QEs.append(QE)

    print("average QE:", sum(QEs)/len(QEs))