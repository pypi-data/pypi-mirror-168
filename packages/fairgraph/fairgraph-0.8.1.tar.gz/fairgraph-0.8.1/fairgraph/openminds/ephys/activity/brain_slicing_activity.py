"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base_v3 import KGObject, IRI
from fairgraph.fields import Field




class BrainSlicingActivity(KGObject):
    """

    """
    default_space = "electrophysiology"
    type = ["https://openminds.ebrains.eu/ephys/BrainSlicingActivity"]
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
        Field("behavioral_protocols", "openminds.core.BehavioralProtocol", "vocab:behavioralProtocol", multiple=True, required=False,
              doc="no description available"),
        Field("cutting_thickness", ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"], "vocab:cuttingThickness", multiple=False, required=False,
              doc="no description available"),
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the brain slicing activity."),
        Field("ended_at_time", datetime, "vocab:endedAtTime", multiple=False, required=False,
              doc="no description available"),
        Field("inputs", "openminds.core.SubjectState", "vocab:input", multiple=True, required=True,
              doc="Something or someone that is put into or participates in a process or machine."),
        Field("is_part_of", "openminds.core.DatasetVersion", "vocab:isPartOf", multiple=False, required=True,
              doc="Reference to the ensemble of multiple things or beings."),
        Field("outputs", "openminds.core.TissueSampleState", "vocab:output", multiple=True, required=True,
              doc="Something or someone that comes out of, is delivered or produced by a process or machine."),
        Field("parameter_sets", "openminds.core.ParameterSet", "vocab:parameterSet", multiple=True, required=False,
              doc="Manner, position, or direction in which digital or physical properties are set to determine a particular function, characteristics or behavior of something."),
        Field("preparation_design", "openminds.controlledterms.PreparationType", "vocab:preparationDesign", multiple=False, required=False,
              doc="no description available"),
        Field("protocols", "openminds.core.Protocol", "vocab:protocol", multiple=True, required=True,
              doc="Plan that describes the process of a scientific or medical experiment, treatment, or procedure."),
        Field("slicing_angle", ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"], "vocab:slicingAngle", multiple=False, required=False,
              doc="no description available"),
        Field("slicing_plane", "openminds.controlledterms.AnatomicalPlane", "vocab:slicingPlane", multiple=False, required=False,
              doc="no description available"),
        Field("solution", str, "vocab:solution", multiple=False, required=False,
              doc="no description available"),
        Field("started_at_time", datetime, "vocab:startedAtTime", multiple=False, required=False,
              doc="no description available"),
        Field("study_targets", ["openminds.controlledterms.BiologicalOrder", "openminds.controlledterms.BiologicalSex", "openminds.controlledterms.BreedingType", "openminds.controlledterms.CellCultureType", "openminds.controlledterms.CellType", "openminds.controlledterms.Disease", "openminds.controlledterms.DiseaseModel", "openminds.controlledterms.GeneticStrainType", "openminds.controlledterms.Handedness", "openminds.controlledterms.MolecularEntity", "openminds.controlledterms.Organ", "openminds.controlledterms.Species", "openminds.controlledterms.SubcellularEntity", "openminds.controlledterms.TermSuggestion", "openminds.controlledterms.UBERONParcellation", "openminds.sands.CustomAnatomicalEntity", "openminds.sands.ParcellationEntity", "openminds.sands.ParcellationEntityVersion"], "vocab:studyTarget", multiple=True, required=False,
              doc="Structure or function that was targeted within a study."),

    ]
    existence_query_fields = ('lookup_label',)
