#
# Model thông tin file DICOM hiện thị ra view
#
import pydicom, json

class DicomInfoFormat:
    GroupTag = ""
    ElementTag = ""
    TagDesscription = ""
    Value = ""

    def __init__(self, GroupTag, ElementTag, TagDesscription, Value):
        self.GroupTag = GroupTag
        self.ElementTag = ElementTag
        self.TagDesscription = TagDesscription
        self.Value = Value

class DicomInfo:

    def getInfoJson(self, path):
        ds = pydicom.dcmread(path)
        ketQua = []
        ketQua.append(DicomInfoFormat("0008", "0008", "Image Type", str(ds.ImageType)))
        ketQua.append(DicomInfoFormat("0008", "0012", "Instance Creation Date", str(ds.InstanceCreationDate)))
        ketQua.append(DicomInfoFormat("0008", "0013", "Instance Creation Time", str(ds.InstanceCreationTime)))
        ketQua.append(DicomInfoFormat("0008", "0016", "SOP Class UID", str(ds.SOPClassUID)))

        ketQua.append(DicomInfoFormat("0008", "0018", "SOP Instance UID", str(ds.SOPInstanceUID)))
        ketQua.append(DicomInfoFormat("0008", "0020", "Study Date", str(ds.StudyDate)))
        ketQua.append(DicomInfoFormat("0008", "0022", "Instance Creation Time", str(ds.InstanceCreationTime)))
        ketQua.append(DicomInfoFormat("0008", "0022", "Acquisition Date", str(ds.AcquisitionDate)))

        ketQua.append(DicomInfoFormat("0008", "0023", "Content Date", str(ds.ContentDate)))
        ketQua.append(DicomInfoFormat("0008", "0030", "Acquisition Date", str(ds.StudyTime)))
        ketQua.append(DicomInfoFormat("0008", "0032", "Acquisition Time", str(ds.AcquisitionTime)))
        ketQua.append(DicomInfoFormat("0008", "0033", "Content Time", str(ds.ContentTime)))

        ketQua.append(DicomInfoFormat("0008", "0050", "Accession Number", str(ds.AccessionNumber)))
        ketQua.append(DicomInfoFormat("0008", "0060", "Modality", str(ds.Modality)))
        ketQua.append(DicomInfoFormat("0008", "0070", "Manufacturer", str(ds.Manufacturer)))
        ketQua.append(DicomInfoFormat("0008", "0080", "Institution Name", str(ds.InstitutionName)))

        ketQua.append(DicomInfoFormat("0008", "0081", "Institution Address", str(ds.InstitutionAddress)))
        ketQua.append(DicomInfoFormat("0008", "103e", "Series Description", str(ds.SeriesDescription)))
        ketQua.append(DicomInfoFormat("0008", "1010", "Station Name", str(ds.StationName)))
        ketQua.append(DicomInfoFormat("0008", "1030", "Study Description", str(ds.StudyDescription)))

        ketQua.append(DicomInfoFormat("0010", "0010", "Patient Name", str(ds.PatientName)))
        ketQua.append(DicomInfoFormat("0010", "0020", "Patient ID", str(ds.PatientID)))
        ketQua.append(DicomInfoFormat("0010", "0030", "Patient Birth Date", str(ds.PatientBirthDate)))
        ketQua.append(DicomInfoFormat("0010", "0040", "Patient Sex", str(ds.PatientSex)))

        ketQua.append(DicomInfoFormat("0010", "1010", "Patient Age", str(ds.PatientAge)))
        ketQua.append(DicomInfoFormat("0010", "2000", "Medical Alerts", str(ds.MedicalAlerts)))
        ketQua.append(DicomInfoFormat("0018", "0022", "Scan Options", str(ds.ScanOptions)))
        ketQua.append(DicomInfoFormat("0018", "0050", "Slice Thickness", str(ds.SliceThickness)))

        ketQua.append(DicomInfoFormat("0018", "0060", "KVP", str(ds.KVP)))
        ketQua.append(DicomInfoFormat("0018", "0088", "Spacing Between Slices", str(ds.SpacingBetweenSlices)))
        ketQua.append(DicomInfoFormat("0018", "0090", "Data Collection Diameter", str(ds.DataCollectionDiameter)))
        ketQua.append(DicomInfoFormat("0018", "1030", "Protocol Name", str(ds.ProtocolName)))

        ketQua.append(DicomInfoFormat("0018", "1100", "Reconstruction Diameter", str(ds.ReconstructionDiameter)))
        ketQua.append(DicomInfoFormat("0018", "1120", "Gantry Detector Tilt", str(ds.GantryDetectorTilt)))
        ketQua.append(DicomInfoFormat("0018", "1130", "Table Height", str(ds.TableHeight)))
        ketQua.append(DicomInfoFormat("0018", "1140", "Rotation Direction", str(ds.RotationDirection)))

        ketQua.append(DicomInfoFormat("0018", "1151", "XRay TubeCurrent", str(ds.XRayTubeCurrent)))
        ketQua.append(DicomInfoFormat("0018", "1152", "Exposure", str(ds.Exposure)))
        ketQua.append(DicomInfoFormat("0018", "1160", "Filter Type", str(ds.FilterType)))
        ketQua.append(DicomInfoFormat("0018", "1210", "Convolution Kernel", str(ds.ConvolutionKernel)))

        ketQua.append(DicomInfoFormat("0018", "5100", "Patient Position", str(ds.PatientPosition)))
        ketQua.append(DicomInfoFormat("0018", "9323", "Exposure Modulation Type", str(ds.ExposureModulationType)))
        ketQua.append(DicomInfoFormat("0018", "9345", "CTDIvol", str(ds.CTDIvol)))
        ketQua.append(DicomInfoFormat("0020", "000d", "Study Instance UID", str(ds.StudyInstanceUID)))

        ketQua.append(DicomInfoFormat("0020", "000e", "Series Instance UID", str(ds.SeriesInstanceUID)))
        ketQua.append(DicomInfoFormat("0020", "0010", "Study ID", str(ds.StudyID)))
        ketQua.append(DicomInfoFormat("0020", "0011", "Series Number", str(ds.SeriesNumber)))
        ketQua.append(DicomInfoFormat("0020", "0012", "Acquisition Number", str(ds.AcquisitionNumber)))

        ketQua.append(DicomInfoFormat("0020", "0013", "Instance Number", str(ds.InstanceNumber)))
        ketQua.append(DicomInfoFormat("0020", "0032", "Image Position Patient", str(ds.ImagePositionPatient)))
        ketQua.append(DicomInfoFormat("0020", "0037", "Image Orientation Patient", str(ds.ImageOrientationPatient)))
        ketQua.append(DicomInfoFormat("0020", "0052", "Frame Of Reference UID", str(ds.FrameOfReferenceUID)))
        
        ketQua.append(DicomInfoFormat("0020", "0060", "Laterality", str(ds.Laterality)))
        ketQua.append(DicomInfoFormat("0020", "1040", "Position Reference Indicator", str(ds.PositionReferenceIndicator)))
        ketQua.append(DicomInfoFormat("0020", "1041", "Slice Location", str(ds.SliceLocation)))
        ketQua.append(DicomInfoFormat("0020", "4000", "Image Comments", str(ds.ImageComments)))

        ketQua.append(DicomInfoFormat("0028", "0004", "Photometric Interpretation", str(ds.PhotometricInterpretation)))
        ketQua.append(DicomInfoFormat("0028", "0010", "Rows", str(ds.Rows)))
        ketQua.append(DicomInfoFormat("0028", "0011", "Columns", str(ds.Columns)))
        ketQua.append(DicomInfoFormat("0028", "0030", "Pixel Spacing", str(ds.PixelSpacing)))

        ketQua.append(DicomInfoFormat("0028", "0100", "Bits Allocated", str(ds.BitsAllocated)))
        ketQua.append(DicomInfoFormat("0028", "0101", "Bits Stored", str(ds.BitsStored)))
        ketQua.append(DicomInfoFormat("0028", "0102", "High Bit", str(ds.HighBit)))
        ketQua.append(DicomInfoFormat("0028", "0103", "Pixel Representation", str(ds.PixelRepresentation)))
        
        ketQua.append(DicomInfoFormat("0028", "1050", "Window Center", str(ds.WindowCenter)))
        ketQua.append(DicomInfoFormat("0028", "1051", "Window Width", str(ds.WindowWidth)))
        ketQua.append(DicomInfoFormat("0028", "1052", "Rescale Intercept", str(ds.RescaleIntercept)))
        ketQua.append(DicomInfoFormat("0028", "1053", "RescaleSlope", str(ds.RescaleSlope)))

        ketQua.append(DicomInfoFormat("0032", "1070", "Requested Contrast Agent", str(ds.RequestedContrastAgent)))
        ketQua.append(DicomInfoFormat("0040", "0012", "Pre Medication", str(ds.PreMedication)))
        ketQua.append(DicomInfoFormat("0040", "0253", "Performed Procedure Step ID", str(ds.PerformedProcedureStepID)))
        
        return json.dumps([ob.__dict__ for ob in ketQua])