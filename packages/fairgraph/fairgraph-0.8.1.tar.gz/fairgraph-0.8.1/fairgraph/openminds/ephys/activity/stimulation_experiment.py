"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base_v3 import KGObject, IRI
from fairgraph.fields import Field




class StimulationExperiment(KGObject):
    """

    """
    default_space = "electrophysiology"
    type = ["https://openminds.ebrains.eu/ephys/StimulationExperiment"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("lookup_label", str, "vocab:lookupLabel", multiple=False, required=False,
              doc="no description available"),
        Field("aquisition_devices", ["openminds.ephys.Device", "openminds.ephys.Electrode", "openminds.ephys.ElectrodeArray", "openminds.ephys.Pipette"], "vocab:aquisitionDevice", multiple=True, required=True,
              doc="no description available"),
        Field("behavioral_protocols", "openminds.core.BehavioralProtocol", "vocab:behavioralProtocol", multiple=True, required=False,
              doc="no description available"),
        Field("compensation_current", "openminds.ephys.Measurement", "vocab:compensationCurrent", multiple=False, required=False,
              doc="no description available"),
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the stimulation experiment."),
        Field("ended_at_time", datetime, "vocab:endedAtTime", multiple=False, required=False,
              doc="no description available"),
        Field("inputs", ["openminds.core.SubjectGroupState", "openminds.core.SubjectState", "openminds.core.TissueSampleCollectionState", "openminds.core.TissueSampleState", "openminds.ephys.PatchedCell"], "vocab:input", multiple=True, required=True,
              doc="Something or someone that is put into or participates in a process or machine."),
        Field("input_resistance", "openminds.ephys.Measurement", "vocab:inputResistance", multiple=False, required=False,
              doc="no description available"),
        Field("internal_identifier", str, "vocab:internalIdentifier", multiple=False, required=False,
              doc="Term or code that identifies the stimulation experiment within a particular product."),
        Field("is_part_of", "openminds.core.DatasetVersion", "vocab:isPartOf", multiple=False, required=True,
              doc="Reference to the ensemble of multiple things or beings."),
        Field("measured_holding_potential", "openminds.ephys.Measurement", "vocab:measuredHoldingPotential", multiple=False, required=False,
              doc="no description available"),
        Field("outputs", "openminds.ephys.Recording", "vocab:output", multiple=True, required=True,
              doc="Something or someone that comes out of, is delivered or produced by a process or machine."),
        Field("parameter_sets", "openminds.core.ParameterSet", "vocab:parameterSet", multiple=True, required=False,
              doc="Manner, position, or direction in which digital or physical properties are set to determine a particular function, characteristics or behavior of something."),
        Field("preparation_design", "openminds.controlledterms.PreparationType", "vocab:preparationDesign", multiple=False, required=False,
              doc="no description available"),
        Field("protocols", "openminds.core.Protocol", "vocab:protocol", multiple=True, required=True,
              doc="Plan that describes the process of a scientific or medical experiment, treatment, or procedure."),
        Field("series_resistance", "openminds.ephys.Measurement", "vocab:seriesResistance", multiple=False, required=False,
              doc="no description available"),
        Field("started_at_time", datetime, "vocab:startedAtTime", multiple=False, required=False,
              doc="no description available"),
        Field("stimulation_devices", ["openminds.ephys.Device", "openminds.ephys.Electrode", "openminds.ephys.ElectrodeArray", "openminds.ephys.Pipette"], "vocab:stimulationDevice", multiple=True, required=True,
              doc="no description available"),
        Field("stimulus", "openminds.core.Stimulation", "vocab:stimulus", multiple=False, required=True,
              doc="no description available"),
        Field("study_targets", ["openminds.controlledterms.BiologicalOrder", "openminds.controlledterms.BiologicalSex", "openminds.controlledterms.BreedingType", "openminds.controlledterms.CellCultureType", "openminds.controlledterms.CellType", "openminds.controlledterms.Disease", "openminds.controlledterms.DiseaseModel", "openminds.controlledterms.GeneticStrainType", "openminds.controlledterms.Handedness", "openminds.controlledterms.MolecularEntity", "openminds.controlledterms.Organ", "openminds.controlledterms.Species", "openminds.controlledterms.SubcellularEntity", "openminds.controlledterms.TermSuggestion", "openminds.controlledterms.UBERONParcellation", "openminds.sands.CustomAnatomicalEntity", "openminds.sands.ParcellationEntity", "openminds.sands.ParcellationEntityVersion"], "vocab:studyTarget", multiple=True, required=False,
              doc="Structure or function that was targeted within a study."),
        Field("target_holding_potential", ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"], "vocab:targetHoldingPotential", multiple=False, required=False,
              doc="no description available"),

    ]
    existence_query_fields = ('lookup_label',)
