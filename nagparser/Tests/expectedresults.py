"""Generate expected results for testing."""
import os
import pickle


def buildexpectedresults(nag):
    """Build expected results from a Nag object."""
    expectedresultsfolder = os.path.join(os.path.dirname(__file__), 'ExpectedResults')
    
    # Ensure directory exists
    os.makedirs(expectedresultsfolder, exist_ok=True)
    
    # Save with binary mode for Python 3
    with open(os.path.join(expectedresultsfolder, 'nag_attributes.pickle'), 'wb') as f:
        pickle.dump(nag.attributes, f)


if __name__ == '__main__':
    from nagparser import parse, NagConfig
    
    # Build test config
    testdata_dir = os.path.join(os.path.dirname(__file__), 'testdata')
    files = [
        os.path.join(testdata_dir, 'test_objects.cache'),
        os.path.join(testdata_dir, 'test_status.dat')
    ]
    nagconfig = NagConfig(files)
    nag = parse(nagconfig)
    
    buildexpectedresults(nag)
    print('Expected results generated successfully')
