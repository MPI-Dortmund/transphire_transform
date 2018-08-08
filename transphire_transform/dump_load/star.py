"""
MIT License

Copyright (c) 2018 Max Planck Institute of Molecular Physiology

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from typing import List, Tuple
import pandas as pd # type: ignore
from . import util


def create_star_header(names: List[str]) -> List[str]:
    """
    Create a header for a relion star file.

    Arguments:
    names - List or array of header names

    Returns:
    Header string
    """
    output_list: List[str] = [
        '',
        'data_',
        '',
        'loop_',
        ]
    output_list.extend(util.create_header(names=names, index=True))
    return output_list


def dump_star(file_name: str, data: pd.DataFrame) -> None:
    """
    Create a relion star file.

    Arguments:
    file_name - File name to export
    data - Data to export

    Returns:
    None
    """
    header: List[str] = create_star_header(names=data.keys())
    util.dump_file(
        file_name=file_name,
        data=data,
        header=header,
        vertical=True
        )


def load_star_header(file_name: str) -> Tuple[List[str], int]:
    """
    Load the header information.

    Arguments:
    file_name - Path to the file that contains the header.

    Returns:
    List of header names, rows that are occupied by the header.
    """
    start_header: bool = False
    header_names: List[str] = []
    idx: int

    with open(file_name, 'r') as read:
        for idx, line in enumerate(read.readlines()):
            if line.startswith('_'):
                if start_header:
                    header_names.append(line.strip().split()[0])
                else:
                    start_header = True
                    header_names.append(line.strip().split()[0])
            elif start_header:
                break

    if not start_header:
        raise IOError(f'No header information found in {file_name}')

    return header_names, idx


def load_star(file_name: str) -> pd.DataFrame:
    """
    Load a relion star file.

    Arguments:
    file_name - Path to the relion star file

    Returns:
    Pandas dataframe containing the star file
    """
    header_names: List[str]
    skip_index: int
    star_data: pd.DataFrame

    header_names, skip_index = load_star_header(file_name=file_name)
    star_data = util.load_file(file_name, names=header_names, skiprows=skip_index)
    return star_data


def get_relion_keys(version: int) -> Tuple[str, ...]:
    """
    Get the header keys used by the relion version.

    Arguments:
    version - Version number of relion (2 or 3 supported)

    Returns:
    Tuple of keys
    """
    keys_tuple: Tuple[str, ...]
    if version == 2:
        keys_tuple = keys_relion_2()
    elif version == 3:
        keys_tuple = keys_relion_3()
    else:
        assert False, f'Relion version {version} not implemented, yet.'

    return keys_tuple


def keys_relion_2() -> Tuple[str, ...]:
    """
    Keys for the Relion 2 software.

    Arguments:
    None

    Returns:
    Tuple of keys
    """
    # pylint: disable=C0301
    keys_tuple: Tuple[str, ...] = (
        "_rlnComment", #"A metadata comment (This is treated in a special way)")

        "_rlnAreaId", #"ID (i.e. a unique number) of an area (i.e. field-of-view)")
        "_rlnAreaName", # "Name of an area (i.e. field-of-view)");

        "_rlnCtfBfactor", # "B-factor (in A^2) that describes CTF power spectrum fall-off");
        "_rlnCtfMaxResolution", # "Estimated maximum resolution (in A) of significant CTF Thon rings");
        "_rlnCtfValidationScore", # "Gctf-based validation score for the quality of the CTF fit");
        "_rlnCtfScalefactor", # "Linear scale-factor on the CTF (values between 0 and 1)");
        "_rlnVoltage", # "Voltage of the microscope (in kV)");
        "_rlnDefocusU", # "Defocus in U-direction (in Angstroms, positive values for underfocus)");
        "_rlnDefocusV", # "Defocus in V-direction (in Angstroms, positive values for underfocus)");
        "_rlnDefocusAngle", # "Angle between X and defocus U direction (in degrees)");
        "_rlnSphericalAberration", # "Spherical aberration (in millimeters)");
        "_rlnChromaticAberration", # "Chromatic aberration (in millimeters)");
        "_rlnDetectorPixelSize", # "Pixel size of the detector (in micrometers)");
        "_rlnEnergyLoss", # "Energy loss (in eV)");
        "_rlnCtfFigureOfMerit", # "Figure of merit for the fit of the CTF (not used inside relion_refine)");
        "_rlnCtfImage", # "Name of an image with all CTF values");
        "_rlnLensStability", # "Lens stability (in ppm)");
        "_rlnMagnification", # "Magnification at the detector (in times)");
        "_rlnPhaseShift", # "Phase-shift from a phase-plate (in degrees)");
        "_rlnConvergenceCone", # "Convergence cone (in mrad)");
        "_rlnLongitudinalDisplacement", # "Longitudinal displacement (in Angstroms)");
        "_rlnTransversalDisplacement", # "Transversal displacement (in Angstroms)");
        "_rlnAmplitudeContrast", # "Amplitude contrast (as a fraction, i.e. 10% = 0.1)");
        "_rlnCtfValue", # "Value of the Contrast Transfer Function");

        "_rlnImageName", # "Name of an image");
        "_rlnImageOriginalName", # "Original name of an image");
        "_rlnReconstructImageName", # "Name of an image to be used for reconstruction only");
        "_rlnImageId", # "ID (i.e. a unique number) of an image");
        "_rlnEnabled", # "Not used in RELION, only included for backward compatibility with XMIPP selfiles");
        "_rlnDataType", # "Type of data stored in an image (e.g. int, RFLOAT etc)");
        "_rlnImageDimensionality", # "Dimensionality of data stored in an image (i.e. 2 or 3)");
        "_rlnBeamTiltX", # "Beam tilt in the X-direction (in mrad)");
        "_rlnBeamTiltY", # "Beam tilt in the Y-direction (in mrad)");
        "_rlnBeamTiltGroupName", # "Name of a group (of images) with assumedly identical beam-tilts");
        "_rlnCoordinateX", # "X-Position of an image in a micrograph (in pixels)");
        "_rlnCoordinateY", # "Y-Position of an image in a micrograph (in pixels)");
        "_rlnCoordinateZ", # "Z-Position of an image in a 3D micrograph, i.e. tomogram (in pixels)");
        "_rlnMovieFrameNumber", # "Number of a movie frame");
        "_rlnNormCorrection", # "Normalisation correction value for an image");
        "_rlnMagnificationCorrection", # "Magnification correction value for an image");
        "_rlnSamplingRate", # "Sampling rate of an image (in Angstrom/pixel)");
        "_rlnSamplingRateX", # "Sampling rate in X-direction of an image (in Angstrom/pixel)");
        "_rlnSamplingRateY", # "Sampling rate in Y-direction of an image (in Angstrom/pixel)");
        "_rlnSamplingRateZ", # "Sampling rate in Z-direction of an image (in Angstrom/pixel)");
        "_rlnImageSize", # "Size of an image (in pixels)");
        "_rlnImageSizeX", # "Size of an image in the X-direction (in pixels)");
        "_rlnImageSizeY", # "Size of an image in the Y-direction (in pixels)");
        "_rlnImageSizeZ", # "Size of an image in the Z-direction (in pixels)");
        "_rlnMinimumValue", # "Minimum value for the pixels in an image");
        "_rlnMaximumValue", # "Maximum value for the pixels in an image");
        "_rlnAverageValue", # "Average value for the pixels in an image");
        "_rlnStandardDeviationValue", # "Standard deviation for the pixel values in an image");
        "_rlnSkewnessValue", # "Skewness (3rd moment) for the pixel values in an image");
        "_rlnKurtosisExcessValue", # "Kurtosis excess (4th moment - 3) for the pixel values in an image");
        "_rlnImageWeight", # "Relative weight of an image");

        "_rlnMaskName", # "Name of an image that contains a [0,1] mask");

        "_rlnMatrix_1_1", # "Matrix element (1,1) of a 3x3 matrix");
        "_rlnMatrix_1_2", # "Matrix element (1,2) of a 3x3 matrix");
        "_rlnMatrix_1_3", # "Matrix element (1,3) of a 3x3 matrix");
        "_rlnMatrix_2_1", # "Matrix element (2,1) of a 3x3 matrix");
        "_rlnMatrix_2_2", # "Matrix element (2,1) of a 3x3 matrix");
        "_rlnMatrix_2_3", # "Matrix element (2,1) of a 3x3 matrix");
        "_rlnMatrix_3_1", # "Matrix element (3,1) of a 3x3 matrix");
        "_rlnMatrix_3_2", # "Matrix element (3,1) of a 3x3 matrix");
        "_rlnMatrix_3_3", # "Matrix element (3,1) of a 3x3 matrix");

        "_rlnMicrographId", # "ID (i.e. a unique number) of a micrograph");
        "_rlnMicrographName", # "Name of a micrograph");
        "_rlnMicrographNameNoDW", # "Name of a micrograph without dose weighting");
        "_rlnMicrographMovieName", # "Name of a micrograph movie stack");
        "_rlnMicrographTiltAngle", # "Tilt angle (in degrees) used to collect a micrograph");
        "_rlnMicrographTiltAxisDirection", # "Direction of the tilt-axis (in degrees) used to collect a micrograph");
        "_rlnMicrographTiltAxisOutOfPlane", # "Out-of-plane angle (in degrees) of the tilt-axis used to collect a micrograph (90=in-plane)");

        "_rlnAccuracyRotations", # "Estimated accuracy (in degrees) with which rotations can be assigned");
        "_rlnAccuracyTranslations", # "Estimated accuracy (in pixels) with which translations can be assigned");
        "_rlnAveragePmax", # "Average value (over all images) of the maxima of the probability distributions");
        "_rlnCurrentResolution", # "Current resolution where SSNR^MAP drops below 1 (in 1/Angstroms)");
        "_rlnCurrentImageSize", # "Current size of the images used in the refinement");
        "_rlnSsnrMap", # "Spectral signal-to-noise ratio as defined for MAP estimation (SSNR^MAP)");
        "_rlnReferenceDimensionality", # "Dimensionality of the references (2D/3D)");
        "_rlnDataDimensionality", # "Dimensionality of the data (2D/3D)");
        "_rlnDiff2RandomHalves", # "Power of the differences between two independent reconstructions from random halves of the data");
        "_rlnEstimatedResolution", # "Estimated resolution (in A) for a reference");
        "_rlnFourierCompleteness", # "Fraction of Fourier components (per resolution shell) with SNR>1");
        "_rlnOverallFourierCompleteness", # "Fraction of all Fourier components up to the current resolution with SNR>1");
        "_rlnGoldStandardFsc", # "Fourier shell correlation between two independent reconstructions from random halves of the data");
        "_rlnGroupName", # "The name of a group of images (e.g. all images from a micrograph)");
        "_rlnGroupNumber", # "The number of a group of images");
        "_rlnGroupNrParticles", # "Number particles in a group of images");
        "_rlnGroupScaleCorrection", # "Intensity-scale correction for a group of images");
        "_rlnNrHelicalAsymUnits", # "How many new helical asymmetric units are there in each box");
        "_rlnHelicalTwist", # "The helical twist (rotation per subunit) in degrees");
        "_rlnHelicalTwistMin", # "Minimum helical twist (in degrees, + for right-handedness)");
        "_rlnHelicalTwistMax", # "Maximum helical twist (in degrees, + for right-handedness)");
        "_rlnHelicalTwistInitialStep", # "Initial step of helical twist search (in degrees)");
        "_rlnHelicalRise", # "The helical rise (translation per subunit) in Angstroms");
        "_rlnHelicalRiseMin", # "Minimum helical rise (in Angstroms)");
        "_rlnHelicalRiseMax", # "Maximum helical rise (in Angstroms)");
        "_rlnHelicalRiseInitialStep", # "Initial step of helical rise search (in Angstroms)");
        "_rlnIsHelix", # "Flag to indicate that helical refinement should be performed");
        "_rlnFourierSpaceInterpolator", # "The kernel used for Fourier-space interpolation (NN=0, linear=1)");
        "_rlnLogLikelihood", # "Value of the log-likelihood target function");
        "_rlnMinRadiusNnInterpolation", #"Minimum radius for NN-interpolation (in Fourier pixels), for smaller radii linear int. is used");
        "_rlnNormCorrectionAverage", # "Average value (over all images) of the normalisation correction values");
        "_rlnNrClasses", # "The number of references (i.e. classes) to be used in refinement");
        "_rlnNrBodies", # "The number of independent rigid bodies to be refined in multi-body refinement");
        "_rlnNrGroups", # "The number of different groups of images (each group has its own noise spectrum, and intensity-scale correction)");
        "_rlnSpectralOrientabilityContribution", # "Spectral SNR contribution to the orientability of individual particles");
        "_rlnOriginalImageSize", # "Original size of the images (in pixels)");
        "_rlnPaddingFactor", # "Oversampling factor for Fourier transforms of the references");
        "_rlnClassDistribution", # "Probability Density Function of the different classes (i.e. fraction of images assigned to each class)");
        "_rlnClassPriorOffsetX", # "Prior in the X-offset for a class (in pixels)");
        "_rlnClassPriorOffsetY", # "Prior in the Y-offset for a class (in pixels)");
        "_rlnOrientationDistribution", # "Probability Density Function of the orientations  (i.e. fraction of images assigned to each orient)");
        "_rlnPixelSize", # "Size of the pixels in the references and images (in Angstroms)");
        "_rlnReferenceSpectralPower", # "Spherical average of the power of the reference");
        "_rlnOrientationalPriorMode", # "Mode for prior distributions on the orientations (0=no prior; 1=(rot,tilt,psi); 2=(rot,tilt); 3=rot; 4=tilt; 5=psi) ");
        "_rlnReferenceImage", # "Name of a reference image");
        "_rlnSGDGradientImage", # "Name of image containing the SGD gradient");
        "_rlnSigmaOffsets", #"Standard deviation in the origin offsets (in Angstroms)");
        "_rlnSigma2Noise", # "Spherical average of the standard deviation in the noise (sigma)");
        "_rlnReferenceSigma2", # "Spherical average of the estimated power in the noise of a reference");
        "_rlnSigmaPriorRotAngle", # "Standard deviation of the prior on the rot (i.e. first Euler) angle");
        "_rlnSigmaPriorTiltAngle", # "Standard deviation of the prior on the tilt (i.e. second Euler) angle");
        "_rlnSigmaPriorPsiAngle", # "Standard deviation of the prior on the psi (i.e. third Euler) angle");
        "_rlnSignalToNoiseRatio", # "Spectral signal-to-noise ratio for a reference");
        "_rlnTau2FudgeFactor", # "Regularisation parameter with which estimates for the power in the references will be multiplied (T in original paper)");
        "_rlnReferenceTau2", # "Spherical average of the estimated power in the signal of a reference");

        "_rlnOverallAccuracyRotations", # "Overall accuracy of the rotational assignments (in degrees)");
        "_rlnOverallAccuracyTranslations", # "Overall accuracy of the translational assignments (in pixels)");
        "_rlnAdaptiveOversampleFraction", # "Fraction of the weights that will be oversampled in a second pass of the adaptive oversampling strategy");
        "_rlnAdaptiveOversampleOrder", # "Order of the adaptive oversampling (0=no oversampling, 1= 2x oversampling; 2= 4x oversampling, etc)");
        "_rlnAutoLocalSearchesHealpixOrder", # "Healpix order (before oversampling) from which autosampling procedure will use local angular searches");
        "_rlnAvailableMemory", # "Available memory per computing node (i.e. per MPI-process)");
        "_rlnBestResolutionThusFar", # "The highest resolution that has been obtained in this optimization thus far");
        "_rlnCoarseImageSize", # "Current size of the images to be used in the first pass of the adaptive oversampling strategy (may be smaller than the original image size)");
        "_rlnChangesOptimalOffsets", # "The average change in optimal translation in the last iteration (in pixels) ");
        "_rlnChangesOptimalOrientations", # "The average change in optimal orientation in the last iteration (in degrees) ");
        "_rlnChangesOptimalClasses", # "The number of particles that changed their optimal clsas assignment in the last iteration");
        "_rlnCtfDataArePhaseFlipped", # "Flag to indicate that the input images have been phase-flipped");
        "_rlnCtfDataAreCtfPremultiplied", # "Flag to indicate that the input images have been premultiplied with their CTF");
        "_rlnExperimentalDataStarFile", # "STAR file with metadata for the experimental images");
        "_rlnDoCorrectCtf", # "Flag to indicate that CTF-correction should be performed");
        "_rlnDoCorrectMagnification", # "Flag to indicate that (per-group) magnification correction should be performed");
        "_rlnDoCorrectNorm", # "Flag to indicate that (per-image) normalisation-error correction should be performed");
        "_rlnDoCorrectScale", # "Flag to indicate that internal (per-group) intensity-scale correction should be performed");
        "_rlnDoRealignMovies", # "Flag to indicate that individual frames of movies are being re-aligned");
        "_rlnDoMapEstimation", # "Flag to indicate that MAP estimation should be performed (otherwise ML estimation)");
        "_rlnDoStochasticGradientDescent", # "Flag to indicate that SGD-optimisation should be performed (otherwise expectation maximisation)");
        "_rlnSgdMuFactor", # "The mu-parameter that controls the momentum of the SGD gradients");
        "_rlnSgdSigma2FudgeInitial", # "The variance of the noise will initially be multiplied with this value (larger than 1)");
        "_rlnSgdSigma2FudgeHalflife", # "After processing this many particles the multiplicative factor for the noise variance will have halved");
        "_rlnSgdNextSubset", # "Number of the next subset to restart this run with");
        "_rlnSgdSubsetSize", # "The number of particles in the random subsets for SGD");
        "_rlnSgdWriteEverySubset", # "Every this many subsets the model is written to disk");
        "_rlnSgdMaxSubsets", # "Stop SGD after doing this many subsets (possibly spanning more than 1 iteration)");
        "_rlnSgdStepsize", # "Stepsize in SGD updates)");
        "_rlnDoAutoRefine", # "Flag to indicate that 3D auto-refine procedure is being used");
        "_rlnDoOnlyFlipCtfPhases", # "Flag to indicate that CTF-correction should only comprise phase-flipping");
        "_rlnDoSolventFlattening", # "Flag to indicate that the references should be masked to set their solvent areas to a constant density");
        "_rlnDoSkipAlign", # "Flag to indicate that orientational (i.e. rotational and translational) searches will be omitted from the refinement, only marginalisation over classes will take place");
        "_rlnDoSkipRotate", # "Flag to indicate that rotational searches will be omitted from the refinement, only marginalisation over classes and translations will take place");
        "_rlnDoSplitRandomHalves", # "Flag to indicate that the data should be split into two completely separate, random halves");
        "_rlnDoZeroMask", # "Flag to indicate that the surrounding solvent area in the experimental particles will be masked to zeros (by default random noise will be used");
        "_rlnFixSigmaNoiseEstimates", # "Flag to indicate that the estimates for the power spectra of the noise should be kept constant");
        "_rlnFixSigmaOffsetEstimates", # "Flag to indicate that the estimates for the stddev in the origin offsets should be kept constant");
        "_rlnFixTauEstimates", # "Flag to indicate that the estimates for the power spectra of the signal (i.e. the references) should be kept constant");
        "_rlnHasConverged", # "Flag to indicate that the optimization has converged");
        "_rlnHasHighFscAtResolLimit", # "Flag to indicate that the FSC at the resolution limit is significant");
        "_rlnHasLargeSizeIncreaseIterationsAgo", # "How many iterations have passed since the last large increase in image size");
        "_rlnDoHelicalRefine", # "Flag to indicate that helical refinement should be performed");
        "_rlnIgnoreHelicalSymmetry", # "Flag to indicate that helical symmetry is ignored in 3D reconstruction");
        "_rlnHelicalTwistInitial", # "The intial helical twist (rotation per subunit) in degrees before refinement");
        "_rlnHelicalRiseInitial", # "The initial helical rise (translation per subunit) in Angstroms before refinement");
        "_rlnHelicalCentralProportion", # "Only expand this central fraction of the Z axis when imposing real-space helical symmetry");
        "_rlnHelicalMaskTubeInnerDiameter", # "Inner diameter of helical tubes in Angstroms (for masks of helical references and particles)");
        "_rlnHelicalMaskTubeOuterDiameter", # "Outer diameter of helical tubes in Angstroms (for masks of helical references and particles)");
        "_rlnHelicalSymmetryLocalRefinement", # "Flag to indicate that local refinement of helical parameters should be performed");
        "_rlnHelicalSigmaDistance", # "Sigma of distance along the helical tracks");
        "_rlnHelicalKeepTiltPriorFixed", # "Flag to indicate that helical tilt priors are kept fixed (at 90 degrees) in global angular searches");
        "_rlnHighresLimitExpectation", # "High-resolution-limit (in Angstrom) for the expectation step");
        "_rlnHighresLimitSGD", # "High-resolution-limit (in Angstrom) for Stochastic Gradient Descent");
        "_rlnDoIgnoreCtfUntilFirstPeak", # "Flag to indicate that the CTFs should be ignored until their first peak");
        "_rlnIncrementImageSize", # "Number of Fourier shells to be included beyond the resolution where SSNR^MAP drops below 1");
        "_rlnCurrentIteration", # "The number of the current iteration");
        "_rlnLocalSymmetryFile", # "Local symmetry description file containing list of masks and their operators");
        "_rlnJoinHalvesUntilThisResolution", # "Resolution (in Angstrom) to join the two random half-reconstructions to prevent their diverging orientations (for C-symmetries)");
        "_rlnMagnificationSearchRange", # "Search range for magnification correction");
        "_rlnMagnificationSearchStep", # "Step size  for magnification correction");
        "_rlnMaximumCoarseImageSize", # "Maximum size of the images to be used in the first pass of the adaptive oversampling strategy (may be smaller than the original image size)");
        "_rlnMaxNumberOfPooledParticles", # "Maximum number particles that are processed together to speed up calculations");
        "_rlnModelStarFile", # "STAR file with metadata for the model that is being refined");
        "_rlnModelStarFile2", # "STAR file with metadata for the second model that is being refined (from random halves of the data)");
        "_rlnNumberOfIterations", # "Maximum number of iterations to be performed");
        "_rlnNumberOfIterWithoutResolutionGain", # "Number of iterations that have passed without a gain in resolution");
        "_rlnNumberOfIterWithoutChangingAssignments", # "Number of iterations that have passed without large changes in orientation and class assignments");
        "_rlnOutputRootName", # "Rootname for all output files (this may include a directory structure, which should then exist)");
        "_rlnParticleDiameter", # "Diameter of the circular mask to be applied to all experimental images (in Angstroms)");
        "_rlnRadiusMaskMap", # "Radius of the spherical mask to be applied to all references (in Angstroms)");
        "_rlnRadiusMaskExpImages", # "Radius of the circular mask to be applied to all experimental images (in Angstroms)");
        "_rlnRandomSeed", # "Seed (i.e. a number) for the random number generator");
        "_rlnRefsAreCtfCorrected", # "Flag to indicate that the input references have been CTF-amplitude corrected");
        "_rlnSmallestChangesClasses", # "Smallest changes thus far in the optimal class assignments (in numer of particles).");
        "_rlnSmallestChangesOffsets", # "Smallest changes thus far in the optimal offset assignments (in pixels).");
        "_rlnSmallestChangesOrientations", # "Smallest changes thus far in the optimal orientation assignments (in degrees).");
        "_rlnOrientSamplingStarFile", # "STAR file with metadata for the orientational sampling");
        "_rlnSolventMaskName", # "Name of an image that contains a (possibly soft) mask for the solvent area (values=0 for solvent, values =1 for protein)");
        "_rlnSolventMask2Name", # "Name of a secondary solvent mask (e.g. to flatten density inside an icosahedral virus)");
        "_rlnTauSpectrumName", # "Name of a STAR file that holds a tau2-spectrum");
        "_rlnUseTooCoarseSampling", # "Flag to indicate that the angular sampling on the sphere will be one step coarser than needed to speed up calculations");
        "_rlnWidthMaskEdge", # "Width (in pixels) of the soft edge for spherical/circular masks to be used for solvent flattening");

        "_rlnIsFlip", # "Flag to indicate that an image should be mirrored");
        "_rlnOrientationsID", # "ID (i.e. a unique number) for an orientation");
        "_rlnOriginX", # "X-coordinate (in pixels) for the origin of rotation");
        "_rlnOriginXPrior", # "Center of the prior on the X-coordinate (in pixels) for the origin of rotation");
        "_rlnOriginY", # "Y-coordinate (in pixels) for the origin of rotation");
        "_rlnOriginYPrior", # "Center of the prior on the X-coordinate (in pixels) for the origin of rotation");
        "_rlnOriginZ", # "Z-coordinate (in pixels) for the origin of rotation");
        "_rlnOriginZPrior", # "Center of the prior on the X-coordinate (in pixels) for the origin of rotation");
        "_rlnAngleRot", # "First Euler angle (rot, in degrees)");
        "_rlnAngleRotPrior", # "Center of the prior (in degrees) on the first Euler angle (rot)");
        "_rlnAngleTilt", # "Second Euler angle (tilt, in degrees)");
        "_rlnAngleTiltPrior", # "Center of the prior (in degrees) on the second Euler angle (tilt)");
        "_rlnAnglePsi", # "Third Euler, or in-plane angle (psi, in degrees)");
        "_rlnAnglePsiPrior", # "Center of the prior (in degrees) on the third Euler angle (psi)");
        "_rlnAnglePsiFlipRatio", # "Flip ratio of bimodal psi prior (0~0.5, 0 means an ordinary prior, 0.5 means a perfect bimodal prior)");

        "_rlnAutopickFigureOfMerit", # "Autopicking FOM for a particle");
        "_rlnHelicalTubeID", # "Helical tube ID for a helical segment");
        "_rlnHelicalTubePitch", # "Corss-over distance for a helical segment (A)");
        "_rlnHelicalTrackLength", # "Distance from the position of this helical segment to the starting point of the tube");
        "_rlnClassNumber", # "Class number for which a particle has its highest probability");
        "_rlnLogLikeliContribution", # "Contribution of a particle to the log-likelihood target function");
        "_rlnParticleId", # "ID (i.e. a unique number) for a particle");
        "_rlnParticleFigureOfMerit", # "Developmental FOM for a particle");
        "_rlnKullbackLeibnerDivergence", # "Kullback-Leibner divergence for a particle");
        "_rlnRandomSubset", # "Random subset to which this particle belongs");
        "_rlnParticleName", # "Name for a particles");
        "_rlnOriginalParticleName", # "Original name for a particles");
        "_rlnNrOfSignificantSamples", # "Number of orientational/class assignments (for a particle) with sign.probabilities in the 1st pass of adaptive oversampling"); /**< particle, Number of orientations contributing to weights*/
        "_rlnNrOfFrames", # "Number of movie frames that were collected for this particle");
        "_rlnAverageNrOfFrames", # "Number of movie frames that one averages over upon extraction of movie-particles");
        "_rlnMovieFramesRunningAverage", # "Number of movie frames inside the running average that will be used for movie-refinement");
        "_rlnMaxValueProbDistribution", # "Maximum value of the (normalised) probability function for a particle"); /**< particle, Maximum value of probability distribution */

        "_rlnPipeLineJobCounter", # "Number of the last job in the pipeline");
        "_rlnPipeLineNodeName", # "Name of a Node in the pipeline");
        "_rlnPipeLineNodeType", # "Type of a Node in the pipeline");
        "_rlnPipeLineProcessAlias", # "Alias of a Process in the pipeline");
        "_rlnPipeLineProcessName", # "Name of a Process in the pipeline");
        "_rlnPipeLineProcessType", # "Type of a Process in the pipeline");
        "_rlnPipeLineProcessStatus", # "Status of a Process in the pipeline (running, scheduled, finished or cancelled)");
        "_rlnPipeLineEdgeFromNode", # "Name of the origin of an edge");
        "_rlnPipeLineEdgeToNode", # "Name of the to-Node in an edge");
        "_rlnPipeLineEdgeProcess", # "Name of the destination of an edge");

        "_rlnFinalResolution", # "Final estimated resolution after postprocessing (in Angstroms)");
        "_rlnBfactorUsedForSharpening", # "Applied B-factor in the sharpening of the map");
        "_rlnFourierShellCorrelation", # "FSC value (of unspecified type, e.g. masked or unmasked)");
        "_rlnFourierShellCorrelationCorrected", # "Final FSC value: i.e. after correction based on masking of randomized-phases maps");
        "_rlnFourierShellCorrelationMaskedMaps", # "FSC value after masking of the original maps");
        "_rlnFourierShellCorrelationUnmaskedMaps", # "FSC value before masking of the original maps");
        "_rlnCorrectedFourierShellCorrelationPhaseRandomizedMaskedMaps", # "FSC value after masking of the randomized-phases maps");
        "_rlnAmplitudeCorrelationMaskedMaps", # "Correlation coefficient between amplitudes in Fourier shells of masked maps");
        "_rlnAmplitudeCorrelationUnmaskedMaps", # "Correlation coefficient between amplitudes in Fourier shells of unmasked maps");
        "_rlnDifferentialPhaseResidualMaskedMaps", # "Differential Phase Residual in Fourier shells of masked maps");
        "_rlnDifferentialPhaseResidualUnmaskedMaps", # "Differential Phase Residual in Fourier shells of unmasked maps");
        "_rlnFittedInterceptGuinierPlot", # "The fitted intercept of the Guinier-plot");
        "_rlnFittedSlopeGuinierPlot", # "The fitted slope of the Guinier-plot");
        "_rlnCorrelationFitGuinierPlot", # "The correlation coefficient of the fitted line through the Guinier-plot");
        "_rlnLogAmplitudesOriginal", # "Y-value for Guinier plot: the logarithm of the radially averaged amplitudes of the input map");
        "_rlnLogAmplitudesMTFCorrected", # "Y-value for Guinier plot: the logarithm of the radially averaged amplitudes after MTF correction");
        "_rlnLogAmplitudesWeighted", # "Y-value for Guinier plot: the logarithm of the radially averaged amplitudes after FSC-weighting");
        "_rlnLogAmplitudesSharpened", # "Y-value for Guinier plot: the logarithm of the radially averaged amplitudes after sharpening");
        "_rlnLogAmplitudesIntercept", # "Y-value for Guinier plot: the fitted plateau of the logarithm of the radially averaged amplitudes");
        "_rlnResolutionSquared", # "X-value for Guinier plot: squared resolution in 1/Angstrom^2");
        "_rlnMtfValue", # "Value of the detectors modulation transfer function (between 0 and 1)");

        "_rlnIs3DSampling", # "Flag to indicate this concerns a 3D sampling ");
        "_rlnIs3DTranslationalSampling", # "Flag to indicate this concerns a x,y,z-translational sampling ");
        "_rlnHealpixOrder", # "Healpix order for the sampling of the first two Euler angles (rot, tilt) on the 3D sphere");
        "_rlnTiltAngleLimit", # "Values to which to limit the tilt angles (positive for keeping side views, negative for keeping top views)");
        "_rlnOffsetRange", # "Search range for the origin offsets (in Angstroms)");
        "_rlnOffsetStep", # "Step size for the searches in the origin offsets (in Angstroms)");
        "_rlnHelicalOffsetStep", # "Step size for the searches of offsets along helical axis (in Angstroms)");
        "_rlnSamplingPerturbInstance", # "Random instance of the random perturbation on the orientational sampling");
        "_rlnSamplingPerturbFactor", # "Factor for random perturbation on the orientational sampling (between 0 no perturbation and 1 very strong perturbation)");
        "_rlnPsiStep", # "Step size (in degrees) for the sampling of the in-plane rotation angle (psi)");
        "_rlnSymmetryGroup", # "Symmetry group (e.g., C1, D7, I2, I5, etc.)");

        "_rlnSelected", # "Flag whether an entry in a metadatatable is selected in the viewer or not");
        "_rlnParticleSelectZScore", # "Sum of Z-scores from particle_select. High Z-scores are likely to be outliers.");
        "_rlnSortedIndex", # "Index of a metadata entry after sorting (first sorted index is 0).");
        "_rlnStarFileMovieParticles", # "Filename of a STAR file with movie-particles in it");
        "_rlnPerFrameCumulativeWeight", # "Sum of the resolution-dependent relative weights from the first frame until the given frame");
        "_rlnPerFrameRelativeWeight", # "The resolution-dependent relative weights for a given frame");

        "_rlnResolution", # "Resolution (in 1/Angstroms)");
        "_rlnAngstromResolution", # "Resolution (in Angstroms)");
        "_rlnResolutionInversePixel", # "Resolution (in 1/pixel, Nyquist = 0.5)");
        "_rlnSpectralIndex", # "Spectral index (i.e. distance in pixels to the origin in Fourier space) ");
        )
    return keys_tuple


def keys_relion_3() -> Tuple[str, ...]:
    """
    Keys for the Relion 3 software.

    Arguments:
    None

    Returns:
    Tuple of keys
    """
    # pylint: disable=C0301
    keys_tuple: Tuple[str, ...] = (
        "_rlnComment", # "A metadata comment (This is treated in a special way)");

        "_rlnAreaId", # "ID (i.e. a unique number) of an area (i.e. field-of-view)");
        "_rlnAreaName", # "Name of an area (i.e. field-of-view)");

        "_rlnBodyMaskName", # "Name of an image that contains a [0,1] body mask for multi-body refinement");
        "_rlnBodyKeepFixed", # "Flag to indicate whether to keep a body fixed (value 1) or keep on refining it (0)");
        "_rlnBodyReferenceName", # "Name of an image that contains the initial reference for one body of a multi-body refinement");
        "_rlnBodyRotateDirectionX", # "X-component of axis around which to rotate this body");
        "_rlnBodyRotateDirectionY", # "Y-component of axis around which to rotate this body");
        "_rlnBodyRotateDirectionZ", # "Z-component of axis around which to rotate this body");
        "_rlnBodyRotateRelativeTo", # "Number of the body relative to which this body rotates (if negative, use rlnBodyRotateDirectionXYZ)");
        "_rlnBodySigmaAngles", # "Width of prior on all three Euler angles of a body in multibody refinement (in degrees)");
        "_rlnBodySigmaOffset", # "Width of prior on origin offsets of a body in multibody refinement (in pixels)");
        "_rlnBodySigmaRot", # "Width of prior on rot angles of a body in multibody refinement (in degrees)");
        "_rlnBodySigmaTilt", # "Width of prior on tilt angles of a body in multibody refinement (in degrees)");
        "_rlnBodySigmaPsi", # "Width of prior on psi angles of a body in multibody refinement (in degrees)");
        "_rlnBodyStarFile", # "Name of STAR file with body masks and metadata");

        "_rlnCtfAstigmatism", # "Absolute value of the difference between defocus in U- and V-direction (in A)");
        "_rlnCtfBfactor", # "B-factor (in A^2) that describes CTF power spectrum fall-off");
        "_rlnCtfMaxResolution", # "Estimated maximum resolution (in A) of significant CTF Thon rings");
        "_rlnCtfValidationScore", # "Gctf-based validation score for the quality of the CTF fit");
        "_rlnCtfScalefactor", # "Linear scale-factor on the CTF (values between 0 and 1)");
        "_rlnVoltage", # "Voltage of the microscope (in kV)");
        "_rlnDefocusU", # "Defocus in U-direction (in Angstroms, positive values for underfocus)");
        "_rlnDefocusV", # "Defocus in V-direction (in Angstroms, positive values for underfocus)");
        "_rlnDefocusAngle", # "Angle between X and defocus U direction (in degrees)");
        "_rlnSphericalAberration", # "Spherical aberration (in millimeters)");
        "_rlnChromaticAberration", # "Chromatic aberration (in millimeters)");
        "_rlnDetectorPixelSize", # "Pixel size of the detector (in micrometers)");
        "_rlnEnergyLoss", # "Energy loss (in eV)");
        "_rlnCtfFigureOfMerit", # "Figure of merit for the fit of the CTF (not used inside relion_refine)");
        "_rlnCtfImage", # "Name of an image with all CTF values");
        "_rlnLensStability", # "Lens stability (in ppm)");
        "_rlnMagnification", # "Magnification at the detector (in times)");
        "_rlnPhaseShift", # "Phase-shift from a phase-plate (in degrees)");
        "_rlnConvergenceCone", # "Convergence cone (in mrad)");
        "_rlnLongitudinalDisplacement", # "Longitudinal displacement (in Angstroms)");
        "_rlnTransversalDisplacement", # "Transversal displacement (in Angstroms)");
        "_rlnAmplitudeContrast", # "Amplitude contrast (as a fraction, i.e. 10% = 0.1)");
        "_rlnCtfValue", # "Value of the Contrast Transfer Function");

        "_rlnImageName", # "Name of an image");
        "_rlnImageOriginalName", # "Original name of an image");
        "_rlnReconstructImageName", # "Name of an image to be used for reconstruction only");
        "_rlnImageId", # "ID (i.e. a unique number) of an image");
        "_rlnEnabled", # "Not used in RELION, only included for backward compatibility with XMIPP selfiles");
        "_rlnDataType", # "Type of data stored in an image (e.g. int, RFLOAT etc)");
        "_rlnImageDimensionality", # "Dimensionality of data stored in an image (i.e. 2 or 3)");
        "_rlnBeamTiltX", # "Beam tilt in the X-direction (in mrad)");
        "_rlnBeamTiltY", # "Beam tilt in the Y-direction (in mrad)");
        "_rlnBeamTiltGroupName", # "Name of a group (of images) with assumedly identical beam-tilts");
        "_rlnCoordinateX", # "X-Position of an image in a micrograph (in pixels)");
        "_rlnCoordinateY", # "Y-Position of an image in a micrograph (in pixels)");
        "_rlnCoordinateZ", # "Z-Position of an image in a 3D micrograph, i.e. tomogram (in pixels)");
        "_rlnMovieFrameNumber", # "Number of a movie frame");
        "_rlnNormCorrection", # "Normalisation correction value for an image");
        "_rlnMagnificationCorrection", # "Magnification correction value for an image");
        "_rlnSamplingRate", # "Sampling rate of an image (in Angstrom/pixel)");
        "_rlnSamplingRateX", # "Sampling rate in X-direction of an image (in Angstrom/pixel)");
        "_rlnSamplingRateY", # "Sampling rate in Y-direction of an image (in Angstrom/pixel)");
        "_rlnSamplingRateZ", # "Sampling rate in Z-direction of an image (in Angstrom/pixel)");
        "_rlnImageSize", # "Size of an image (in pixels)");
        "_rlnImageSizeX", # "Size of an image in the X-direction (in pixels)");
        "_rlnImageSizeY", # "Size of an image in the Y-direction (in pixels)");
        "_rlnImageSizeZ", # "Size of an image in the Z-direction (in pixels)");
        "_rlnMinimumValue", # "Minimum value for the pixels in an image");
        "_rlnMaximumValue", # "Maximum value for the pixels in an image");
        "_rlnAverageValue", # "Average value for the pixels in an image");
        "_rlnStandardDeviationValue", # "Standard deviation for the pixel values in an image");
        "_rlnSkewnessValue", # "Skewness (3rd moment) for the pixel values in an image");
        "_rlnKurtosisExcessValue", # "Kurtosis excess (4th moment - 3) for the pixel values in an image");
        "_rlnImageWeight", # "Relative weight of an image");

        "_rlnMaskName", # "Name of an image that contains a [0,1] mask");

        "_rlnMatrix_1_1", # "Matrix element (1,1) of a 3x3 matrix");
        "_rlnMatrix_1_2", # "Matrix element (1,2) of a 3x3 matrix");
        "_rlnMatrix_1_3", # "Matrix element (1,3) of a 3x3 matrix");
        "_rlnMatrix_2_1", # "Matrix element (2,1) of a 3x3 matrix");
        "_rlnMatrix_2_2", # "Matrix element (2,1) of a 3x3 matrix");
        "_rlnMatrix_2_3", # "Matrix element (2,1) of a 3x3 matrix");
        "_rlnMatrix_3_1", # "Matrix element (3,1) of a 3x3 matrix");
        "_rlnMatrix_3_2", # "Matrix element (3,1) of a 3x3 matrix");
        "_rlnMatrix_3_3", # "Matrix element (3,1) of a 3x3 matrix");

        "_rlnAccumMotionTotal", #"Accumulated global motion during the entire movie (in A)");
        "_rlnAccumMotionEarly", #"Accumulated global motion during the first frames of the movie (in A)");
        "_rlnAccumMotionLate", #"Accumulated global motion during the last frames of the movie (in A)");
        "_rlnMicrographId", # "ID (i.e. a unique number) of a micrograph");
        "_rlnMicrographName", # "Name of a micrograph");
        "_rlnMicrographGainName", # "Name of a gain reference");
        "_rlnMicrographDefectFile", # "Name of a defect list file");
        "_rlnMicrographNameNoDW", # "Name of a micrograph without dose weighting");
        "_rlnMicrographMovieName", # "Name of a micrograph movie stack");
        "_rlnMicrographMetadata", # "Name of a micrograph metadata file");
        "_rlnMicrographTiltAngle", # "Tilt angle (in degrees) used to collect a micrograph");
        "_rlnMicrographTiltAxisDirection", # "Direction of the tilt-axis (in degrees) used to collect a micrograph");
        "_rlnMicrographTiltAxisOutOfPlane", # "Out-of-plane angle (in degrees) of the tilt-axis used to collect a micrograph (90=in-plane)");
        "_rlnMicrographOriginalPixelSize", # "Pixel size of original movie before binning in Angstrom/pixel.");
        "_rlnMicrographPreExposure", # "Pre-exposure dose in electrons per square Angstrom");
        "_rlnMicrographDoseRate", # "Dose rate in electrons per square Angstrom per frame");
        "_rlnMicrographBinning", # "Micrograph binning factor");
        "_rlnMicrographFrameNumber", # "Micrograph frame number");
        "_rlnMotionModelVersion", # "Version of micrograph motion model");
        "_rlnMicrographStartFrame", # "Start frame of a motion model");
        "_rlnMicrographEndFrame", # "End frame of a motion model");
        "_rlnMicrographShiftX", # "X shift of a (patch of) micrograph");
        "_rlnMicrographShiftY", # "Y shift of a (patch of) micrograph");
        "_rlnMotionModelCoeffsIdx", # "Index of a coefficient of a motion model");
        "_rlnMotionModelCoeff", # "A coefficient of a motion model");

        "_rlnAccuracyRotations", # "Estimated accuracy (in degrees) with which rotations can be assigned");
        "_rlnAccuracyTranslations", # "Estimated accuracy (in pixels) with which translations can be assigned");
        "_rlnAveragePmax", # "Average value (over all images) of the maxima of the probability distributions");
        "_rlnCurrentResolution", # "Current resolution where SSNR^MAP drops below 1 (in 1/Angstroms)");
        "_rlnCurrentImageSize", # "Current size of the images used in the refinement");
        "_rlnSsnrMap", # "Spectral signal-to-noise ratio as defined for MAP estimation (SSNR^MAP)");
        "_rlnReferenceDimensionality", # "Dimensionality of the references (2D/3D)");
        "_rlnDataDimensionality", # "Dimensionality of the data (2D/3D)");
        "_rlnDiff2RandomHalves", # "Power of the differences between two independent reconstructions from random halves of the data");
        "_rlnEstimatedResolution", # "Estimated resolution (in A) for a reference");
        "_rlnFourierCompleteness", # "Fraction of Fourier components (per resolution shell) with SNR>1");
        "_rlnOverallFourierCompleteness", # "Fraction of all Fourier components up to the current resolution with SNR>1");
        "_rlnGoldStandardFsc", # "Fourier shell correlation between two independent reconstructions from random halves of the data");
        "_rlnGroupName", # "The name of a group of images (e.g. all images from a micrograph)");
        "_rlnGroupNumber", # "The number of a group of images");
        "_rlnGroupNrParticles", # "Number particles in a group of images");
        "_rlnGroupScaleCorrection", # "Intensity-scale correction for a group of images");
        "_rlnNrHelicalAsymUnits", # "How many new helical asymmetric units are there in each box");
        "_rlnHelicalTwist", # "The helical twist (rotation per subunit) in degrees");
        "_rlnHelicalTwistMin", # "Minimum helical twist (in degrees, + for right-handedness)");
        "_rlnHelicalTwistMax", # "Maximum helical twist (in degrees, + for right-handedness)");
        "_rlnHelicalTwistInitialStep", # "Initial step of helical twist search (in degrees)");
        "_rlnHelicalRise", # "The helical rise (translation per subunit) in Angstroms");
        "_rlnHelicalRiseMin", # "Minimum helical rise (in Angstroms)");
        "_rlnHelicalRiseMax", # "Maximum helical rise (in Angstroms)");
        "_rlnHelicalRiseInitialStep", # "Initial step of helical rise search (in Angstroms)");
        "_rlnIsHelix", # "Flag to indicate that helical refinement should be performed");
        "_rlnFourierSpaceInterpolator", # "The kernel used for Fourier-space interpolation (NN=0, linear=1)");
        "_rlnLogLikelihood", # "Value of the log-likelihood target function");
        "_rlnMinRadiusNnInterpolation", #"Minimum radius for NN-interpolation (in Fourier pixels), for smaller radii linear int. is used");
        "_rlnNormCorrectionAverage", # "Average value (over all images) of the normalisation correction values");
        "_rlnNrClasses", # "The number of references (i.e. classes) to be used in refinement");
        "_rlnNrBodies", # "The number of independent rigid bodies to be refined in multi-body refinement");
        "_rlnNrGroups", # "The number of different groups of images (each group has its own noise spectrum, and intensity-scale correction)");
        "_rlnSpectralOrientabilityContribution", # "Spectral SNR contribution to the orientability of individual particles");
        "_rlnOriginalImageSize", # "Original size of the images (in pixels)");
        "_rlnPaddingFactor", # "Oversampling factor for Fourier transforms of the references");
        "_rlnClassDistribution", # "Probability Density Function of the different classes (i.e. fraction of images assigned to each class)");
        "_rlnClassPriorOffsetX", # "Prior in the X-offset for a class (in pixels)");
        "_rlnClassPriorOffsetY", # "Prior in the Y-offset for a class (in pixels)");
        "_rlnOrientationDistribution", # "Probability Density Function of the orientations  (i.e. fraction of images assigned to each orient)");
        "_rlnPixelSize", # "Size of the pixels in the references and images (in Angstroms)");
        "_rlnReferenceSpectralPower", # "Spherical average of the power of the reference");
        "_rlnOrientationalPriorMode", # "Mode for prior distributions on the orientations (0=no prior; 1=(rot,tilt,psi); 2=(rot,tilt); 3=rot; 4=tilt; 5=psi) ");
        "_rlnReferenceImage", # "Name of a reference image");
        "_rlnSGDGradientImage", # "Name of image containing the SGD gradient");
        "_rlnSigmaOffsets", #"Standard deviation in the origin offsets (in Angstroms)");
        "_rlnSigma2Noise", # "Spherical average of the standard deviation in the noise (sigma)");
        "_rlnReferenceSigma2", # "Spherical average of the estimated power in the noise of a reference");
        "_rlnSigmaPriorRotAngle", # "Standard deviation of the prior on the rot (i.e. first Euler) angle");
        "_rlnSigmaPriorTiltAngle", # "Standard deviation of the prior on the tilt (i.e. second Euler) angle");
        "_rlnSigmaPriorPsiAngle", # "Standard deviation of the prior on the psi (i.e. third Euler) angle");
        "_rlnSignalToNoiseRatio", # "Spectral signal-to-noise ratio for a reference");
        "_rlnTau2FudgeFactor", # "Regularisation parameter with which estimates for the power in the references will be multiplied (T in original paper)");
        "_rlnReferenceTau2", # "Spherical average of the estimated power in the signal of a reference");

        "_rlnOverallAccuracyRotations", # "Overall accuracy of the rotational assignments (in degrees)");
        "_rlnOverallAccuracyTranslations", # "Overall accuracy of the translational assignments (in pixels)");
        "_rlnAdaptiveOversampleFraction", # "Fraction of the weights that will be oversampled in a second pass of the adaptive oversampling strategy");
        "_rlnAdaptiveOversampleOrder", # "Order of the adaptive oversampling (0=no oversampling, 1= 2x oversampling; 2= 4x oversampling, etc)");
        "_rlnAutoLocalSearchesHealpixOrder", # "Healpix order (before oversampling) from which autosampling procedure will use local angular searches");
        "_rlnAvailableMemory", # "Available memory per computing node (i.e. per MPI-process)");
        "_rlnBestResolutionThusFar", # "The highest resolution that has been obtained in this optimization thus far");
        "_rlnCoarseImageSize", # "Current size of the images to be used in the first pass of the adaptive oversampling strategy (may be smaller than the original image size)");
        "_rlnChangesOptimalOffsets", # "The average change in optimal translation in the last iteration (in pixels) ");
        "_rlnChangesOptimalOrientations", # "The average change in optimal orientation in the last iteration (in degrees) ");
        "_rlnChangesOptimalClasses", # "The number of particles that changed their optimal clsas assignment in the last iteration");
        "_rlnCtfDataArePhaseFlipped", # "Flag to indicate that the input images have been phase-flipped");
        "_rlnCtfDataAreCtfPremultiplied", # "Flag to indicate that the input images have been premultiplied with their CTF");
        "_rlnExperimentalDataStarFile", # "STAR file with metadata for the experimental images");
        "_rlnDoCorrectCtf", # "Flag to indicate that CTF-correction should be performed");
        "_rlnDoCorrectMagnification", # "Flag to indicate that (per-group) magnification correction should be performed");
        "_rlnDoCorrectNorm", # "Flag to indicate that (per-image) normalisation-error correction should be performed");
        "_rlnDoCorrectScale", # "Flag to indicate that internal (per-group) intensity-scale correction should be performed");
        "_rlnDoRealignMovies", # "Flag to indicate that individual frames of movies are being re-aligned");
        "_rlnDoMapEstimation", # "Flag to indicate that MAP estimation should be performed (otherwise ML estimation)");
        "_rlnDoStochasticGradientDescent", # "Flag to indicate that SGD-optimisation should be performed (otherwise expectation maximisation)");
        "_rlnDoFastSubsetOptimisation", # "Use subsets of the data in the earlier iterations to speed up convergence");
        "_rlnSgdInitialIterations", # "Number of initial SGD iterations (at rlnSgdInitialResolution and with rlnSgdInitialSubsetSize)");
        "_rlnSgdFinalIterations", # "Number of final SGD iterations (at rlnSgdFinalResolution and with rlnSgdFinalSubsetSize)");
        "_rlnSgdInBetweenIterations", # "Number of SGD iteration in between the initial ones to the final ones (with linear interpolation of resolution and subset size)");
        "_rlnSgdInitialResolution", # "Resolution (in A) to use during the initial SGD iterations");
        "_rlnSgdFinalResolution", # "Resolution (in A) to use during the final SGD iterations");
        "_rlnSgdInitialSubsetSize", # "Number of particles in a mini-batch (subset) during the initial SGD iterations");
        "_rlnSgdFinalSubsetSize", # "Number of particles in a mini-batch (subset) during the final SGD iteration");
        "_rlnSgdMuFactor", # "The mu-parameter that controls the momentum of the SGD gradients");
        "_rlnSgdSigma2FudgeInitial", # "The variance of the noise will initially be multiplied with this value (larger than 1)");
        "_rlnSgdSigma2FudgeHalflife", # "After processing this many particles the multiplicative factor for the noise variance will have halved");
        "_rlnSgdSkipAnneal", # "Option to switch off annealing of multiple references in SGD");
        "_rlnSgdSubsetSize", # "The number of particles in the random subsets for SGD");
        "_rlnSgdWriteEverySubset", # "Every this many iterations the model is written to disk in SGD");
        "_rlnSgdMaxSubsets", # "Stop SGD after doing this many subsets (possibly spanning more than 1 iteration)");
        "_rlnSgdStepsize", # "Stepsize in SGD updates)");
        "_rlnDoAutoRefine", # "Flag to indicate that 3D auto-refine procedure is being used");
        "_rlnDoOnlyFlipCtfPhases", # "Flag to indicate that CTF-correction should only comprise phase-flipping");
        "_rlnDoSolventFlattening", # "Flag to indicate that the references should be masked to set their solvent areas to a constant density");
        "_rlnDoSolventFscCorrection", # "Flag to indicate that the FSCs should be solvent-corrected during refinement");
        "_rlnDoSkipAlign", # "Flag to indicate that orientational (i.e. rotational and translational) searches will be omitted from the refinement, only marginalisation over classes will take place");
        "_rlnDoSkipRotate", # "Flag to indicate that rotational searches will be omitted from the refinement, only marginalisation over classes and translations will take place");
        "_rlnDoSplitRandomHalves", # "Flag to indicate that the data should be split into two completely separate, random halves");
        "_rlnDoZeroMask", # "Flag to indicate that the surrounding solvent area in the experimental particles will be masked to zeros (by default random noise will be used");
        "_rlnFixSigmaNoiseEstimates", # "Flag to indicate that the estimates for the power spectra of the noise should be kept constant");
        "_rlnFixSigmaOffsetEstimates", # "Flag to indicate that the estimates for the stddev in the origin offsets should be kept constant");
        "_rlnFixTauEstimates", # "Flag to indicate that the estimates for the power spectra of the signal (i.e. the references) should be kept constant");
        "_rlnHasConverged", # "Flag to indicate that the optimization has converged");
        "_rlnHasHighFscAtResolLimit", # "Flag to indicate that the FSC at the resolution limit is significant");
        "_rlnHasLargeSizeIncreaseIterationsAgo", # "How many iterations have passed since the last large increase in image size");
        "_rlnDoHelicalRefine", # "Flag to indicate that helical refinement should be performed");
        "_rlnIgnoreHelicalSymmetry", # "Flag to indicate that helical symmetry is ignored in 3D reconstruction");
        "_rlnHelicalTwistInitial", # "The intial helical twist (rotation per subunit) in degrees before refinement");
        "_rlnHelicalRiseInitial", # "The initial helical rise (translation per subunit) in Angstroms before refinement");
        "_rlnHelicalCentralProportion", # "Only expand this central fraction of the Z axis when imposing real-space helical symmetry");
        "_rlnHelicalMaskTubeInnerDiameter", # "Inner diameter of helical tubes in Angstroms (for masks of helical references and particles)");
        "_rlnHelicalMaskTubeOuterDiameter", # "Outer diameter of helical tubes in Angstroms (for masks of helical references and particles)");
        "_rlnHelicalSymmetryLocalRefinement", # "Flag to indicate that local refinement of helical parameters should be performed");
        "_rlnHelicalSigmaDistance", # "Sigma of distance along the helical tracks");
        "_rlnHelicalKeepTiltPriorFixed", # "Flag to indicate that helical tilt priors are kept fixed (at 90 degrees) in global angular searches");
        "_rlnHighresLimitExpectation", # "High-resolution-limit (in Angstrom) for the expectation step");
        "_rlnHighresLimitSGD", # "High-resolution-limit (in Angstrom) for Stochastic Gradient Descent");
        "_rlnDoIgnoreCtfUntilFirstPeak", # "Flag to indicate that the CTFs should be ignored until their first peak");
        "_rlnIncrementImageSize", # "Number of Fourier shells to be included beyond the resolution where SSNR^MAP drops below 1");
        "_rlnCurrentIteration", # "The number of the current iteration");
        "_rlnLocalSymmetryFile", # "Local symmetry description file containing list of masks and their operators");
        "_rlnJoinHalvesUntilThisResolution", # "Resolution (in Angstrom) to join the two random half-reconstructions to prevent their diverging orientations (for C-symmetries)");
        "_rlnMagnificationSearchRange", # "Search range for magnification correction");
        "_rlnMagnificationSearchStep", # "Step size  for magnification correction");
        "_rlnMaximumCoarseImageSize", # "Maximum size of the images to be used in the first pass of the adaptive oversampling strategy (may be smaller than the original image size)");
        "_rlnMaxNumberOfPooledParticles", # "Maximum number particles that are processed together to speed up calculations");
        "_rlnModelStarFile", # "STAR file with metadata for the model that is being refined");
        "_rlnModelStarFile2", # "STAR file with metadata for the second model that is being refined (from random halves of the data)");
        "_rlnNumberOfIterations", # "Maximum number of iterations to be performed");
        "_rlnNumberOfIterWithoutResolutionGain", # "Number of iterations that have passed without a gain in resolution");
        "_rlnNumberOfIterWithoutChangingAssignments", # "Number of iterations that have passed without large changes in orientation and class assignments");
        "_rlnOutputRootName", # "Rootname for all output files (this may include a directory structure, which should then exist)");
        "_rlnParticleDiameter", # "Diameter of the circular mask to be applied to all experimental images (in Angstroms)");
        "_rlnRadiusMaskMap", # "Radius of the spherical mask to be applied to all references (in Angstroms)");
        "_rlnRadiusMaskExpImages", # "Radius of the circular mask to be applied to all experimental images (in Angstroms)");
        "_rlnRandomSeed", # "Seed (i.e. a number) for the random number generator");
        "_rlnRefsAreCtfCorrected", # "Flag to indicate that the input references have been CTF-amplitude corrected");
        "_rlnSmallestChangesClasses", # "Smallest changes thus far in the optimal class assignments (in numer of particles).");
        "_rlnSmallestChangesOffsets", # "Smallest changes thus far in the optimal offset assignments (in pixels).");
        "_rlnSmallestChangesOrientations", # "Smallest changes thus far in the optimal orientation assignments (in degrees).");
        "_rlnOrientSamplingStarFile", # "STAR file with metadata for the orientational sampling");
        "_rlnSolventMaskName", # "Name of an image that contains a (possibly soft) mask for the solvent area (values=0 for solvent, values =1 for protein)");
        "_rlnSolventMask2Name", # "Name of a secondary solvent mask (e.g. to flatten density inside an icosahedral virus)");
        "_rlnTauSpectrumName", # "Name of a STAR file that holds a tau2-spectrum");
        "_rlnUseTooCoarseSampling", # "Flag to indicate that the angular sampling on the sphere will be one step coarser than needed to speed up calculations");
        "_rlnWidthMaskEdge", # "Width (in pixels) of the soft edge for spherical/circular masks to be used for solvent flattening");

        "_rlnIsFlip", # "Flag to indicate that an image should be mirrored");
        "_rlnOrientationsID", # "ID (i.e. a unique number) for an orientation");
        "_rlnOriginX", # "X-coordinate (in pixels) for the origin of rotation");
        "_rlnOriginXPrior", # "Center of the prior on the X-coordinate (in pixels) for the origin of rotation");
        "_rlnOriginY", # "Y-coordinate (in pixels) for the origin of rotation");
        "_rlnOriginYPrior", # "Center of the prior on the X-coordinate (in pixels) for the origin of rotation");
        "_rlnOriginZ", # "Z-coordinate (in pixels) for the origin of rotation");
        "_rlnOriginZPrior", # "Center of the prior on the X-coordinate (in pixels) for the origin of rotation");
        "_rlnAngleRot", # "First Euler angle (rot, in degrees)");
        "_rlnAngleRotPrior", # "Center of the prior (in degrees) on the first Euler angle (rot)");
        "_rlnAngleTilt", # "Second Euler angle (tilt, in degrees)");
        "_rlnAngleTiltPrior", # "Center of the prior (in degrees) on the second Euler angle (tilt)");
        "_rlnAnglePsi", # "Third Euler, or in-plane angle (psi, in degrees)");
        "_rlnAnglePsiPrior", # "Center of the prior (in degrees) on the third Euler angle (psi)");
        "_rlnAnglePsiFlipRatio", # "Flip ratio of bimodal psi prior (0~0.5, 0 means an ordinary prior, 0.5 means a perfect bimodal prior)");

        "_rlnAutopickFigureOfMerit", # "Autopicking FOM for a particle");
        "_rlnHelicalTubeID", # "Helical tube ID for a helical segment");
        "_rlnHelicalTubePitch", # "Cross-over distance for a helical segment (A)");
        "_rlnHelicalTrackLength", # "Distance from the position of this helical segment to the starting point of the tube");
        "_rlnClassNumber", # "Class number for which a particle has its highest probability");
        "_rlnLogLikeliContribution", # "Contribution of a particle to the log-likelihood target function");
        "_rlnParticleId", # "ID (i.e. a unique number) for a particle");
        "_rlnParticleFigureOfMerit", # "Developmental FOM for a particle");
        "_rlnKullbackLeiblerDivergence", # "Kullback-Leibler divergence for a particle");
        "_rlnKullbackLeibnerDivergence", #; // wrong spelling for backwards compatibility
        "_rlnRandomSubset", # "Random subset to which this particle belongs");
        "_rlnBeamTiltClass", # "Beam-tilt class of a particle");
        "_rlnParticleName", # "Name for a particle");
        "_rlnOriginalParticleName", # "Original name for a particles");
        "_rlnNrOfSignificantSamples", # "Number of orientational/class assignments (for a particle) with sign.probabilities in the 1st pass of adaptive oversampling"); /**< particle, Number of orientations contributing to weights*/
        "_rlnNrOfFrames", # "Number of movie frames that were collected for this particle");
        "_rlnAverageNrOfFrames", # "Number of movie frames that one averages over upon extraction of movie-particles");
        "_rlnMovieFramesRunningAverage", # "Number of movie frames inside the running average that will be used for movie-refinement");
        "_rlnMaxValueProbDistribution", # "Maximum value of the (normalised) probability function for a particle"); /**< particle, Maximum value of probability distribution */
        "_rlnParticleNumber", # "Number of particles");

        "_rlnPipeLineJobCounter", # "Number of the last job in the pipeline");
        "_rlnPipeLineNodeName", # "Name of a Node in the pipeline");
        "_rlnPipeLineNodeType", # "Type of a Node in the pipeline");
        "_rlnPipeLineProcessAlias", # "Alias of a Process in the pipeline");
        "_rlnPipeLineProcessName", # "Name of a Process in the pipeline");
        "_rlnPipeLineProcessType", # "Type of a Process in the pipeline");
        "_rlnPipeLineProcessStatus", # "Status of a Process in the pipeline (running, scheduled, finished or cancelled)");
        "_rlnPipeLineEdgeFromNode", # "Name of the origin of an edge");
        "_rlnPipeLineEdgeToNode", # "Name of the to-Node in an edge");
        "_rlnPipeLineEdgeProcess", # "Name of the destination of an edge");

        "_rlnFinalResolution", # "Final estimated resolution after postprocessing (in Angstroms)");
        "_rlnBfactorUsedForSharpening", # "Applied B-factor in the sharpening of the map");
        "_rlnFourierShellCorrelation", # "FSC value (of unspecified type, e.g. masked or unmasked)");
        "_rlnFourierShellCorrelationCorrected", # "Final FSC value: i.e. after correction based on masking of randomized-phases maps");
        "_rlnFourierShellCorrelationMaskedMaps", # "FSC value after masking of the original maps");
        "_rlnFourierShellCorrelationUnmaskedMaps", # "FSC value before masking of the original maps");
        "_rlnCorrectedFourierShellCorrelationPhaseRandomizedMaskedMaps", # "FSC value after masking of the randomized-phases maps");
        "_rlnAmplitudeCorrelationMaskedMaps", # "Correlation coefficient between amplitudes in Fourier shells of masked maps");
        "_rlnAmplitudeCorrelationUnmaskedMaps", # "Correlation coefficient between amplitudes in Fourier shells of unmasked maps");
        "_rlnDifferentialPhaseResidualMaskedMaps", # "Differential Phase Residual in Fourier shells of masked maps");
        "_rlnDifferentialPhaseResidualUnmaskedMaps", # "Differential Phase Residual in Fourier shells of unmasked maps");
        "_rlnFittedInterceptGuinierPlot", # "The fitted intercept of the Guinier-plot");
        "_rlnFittedSlopeGuinierPlot", # "The fitted slope of the Guinier-plot");
        "_rlnCorrelationFitGuinierPlot", # "The correlation coefficient of the fitted line through the Guinier-plot");
        "_rlnLogAmplitudesOriginal", # "Y-value for Guinier plot: the logarithm of the radially averaged amplitudes of the input map");
        "_rlnLogAmplitudesMTFCorrected", # "Y-value for Guinier plot: the logarithm of the radially averaged amplitudes after MTF correction");
        "_rlnLogAmplitudesWeighted", # "Y-value for Guinier plot: the logarithm of the radially averaged amplitudes after FSC-weighting");
        "_rlnLogAmplitudesSharpened", # "Y-value for Guinier plot: the logarithm of the radially averaged amplitudes after sharpening");
        "_rlnLogAmplitudesIntercept", # "Y-value for Guinier plot: the fitted plateau of the logarithm of the radially averaged amplitudes");
        "_rlnResolutionSquared", # "X-value for Guinier plot: squared resolution in 1/Angstrom^2");
        "_rlnMtfValue", # "Value of the detectors modulation transfer function (between 0 and 1)");
        "_rlnRandomiseFrom", # "Resolution (in A) from which the phases are randomised in the postprocessing step");
        "_rlnUnfilteredMapHalf1", # "Name of the unfiltered map from halfset 1");
        "_rlnUnfilteredMapHalf2", # "Name of the unfiltered map from halfset 2");

        "_rlnIs3DSampling", # "Flag to indicate this concerns a 3D sampling ");
        "_rlnIs3DTranslationalSampling", # "Flag to indicate this concerns a x,y,z-translational sampling ");
        "_rlnHealpixOrder", # "Healpix order for the sampling of the first two Euler angles (rot, tilt) on the 3D sphere");
        "_rlnTiltAngleLimit", # "Values to which to limit the tilt angles (positive for keeping side views, negative for keeping top views)");
        "_rlnOffsetRange", # "Search range for the origin offsets (in Angstroms)");
        "_rlnOffsetStep", # "Step size for the searches in the origin offsets (in Angstroms)");
        "_rlnHelicalOffsetStep", # "Step size for the searches of offsets along helical axis (in Angstroms)");
        "_rlnSamplingPerturbInstance", # "Random instance of the random perturbation on the orientational sampling");
        "_rlnSamplingPerturbFactor", # "Factor for random perturbation on the orientational sampling (between 0 no perturbation and 1 very strong perturbation)");
        "_rlnPsiStep", # "Step size (in degrees) for the sampling of the in-plane rotation angle (psi)");
        "_rlnSymmetryGroup", # "Symmetry group (e.g., C1, D7, I2, I5, etc.)");

        "_rlnSelected", # "Flag whether an entry in a metadatatable is selected (1) in the viewer or not (0)");
        "_rlnParticleSelectZScore", # "Sum of Z-scores from particle_select. High Z-scores are likely to be outliers.");
        "_rlnSortedIndex", # "Index of a metadata entry after sorting (first sorted index is 0).");
        "_rlnStarFileMovieParticles", # "Filename of a STAR file with movie-particles in it");
        "_rlnPerFrameCumulativeWeight", # "Sum of the resolution-dependent relative weights from the first frame until the given frame");
        "_rlnPerFrameRelativeWeight", # "The resolution-dependent relative weights for a given frame");

        "_rlnResolution", # "Resolution (in 1/Angstroms)");
        "_rlnAngstromResolution", # "Resolution (in Angstroms)");
        "_rlnResolutionInversePixel", # "Resolution (in 1/pixel, Nyquist = 0.5)");
        "_rlnSpectralIndex", # "Spectral index (i.e. distance in pixels to the origin in Fourier space) ");
        )
    return keys_tuple
