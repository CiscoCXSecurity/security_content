import pytest
import os

from contentctl.contentctl.domain.entities.enums.enums import SecurityContentProduct
from contentctl_infrastructure.contentctl_infrastructure.builder.security_content_detection_builder import SecurityContentDetectionBuilder
from contentctl_infrastructure.contentctl_infrastructure.builder.security_content_basic_builder import SecurityContentBasicBuilder
from contentctl.contentctl.domain.entities.enums.enums import SecurityContentType
from contentctl_infrastructure.contentctl_infrastructure.builder.yml_reader import YmlReader


def test_read_detection():
    security_content_builder = SecurityContentDetectionBuilder()
    security_content_builder.setObject(os.path.join(os.path.dirname(__file__), 
        'test_data/detection/valid.yml'), SecurityContentType.detections)
    detection = security_content_builder.getObject()
    
    assert detection.name == "Attempted Credential Dump From Registry via Reg exe"
    assert detection.author == "Patrick Bareiss, Splunk"


def test_add_deployment_to_detection():
    security_content_builder_deployment = SecurityContentBasicBuilder()
    security_content_builder_deployment.setObject(os.path.join(os.path.dirname(__file__), 
        'test_data/deployment/ESCU/00_default_ttp.yml'), SecurityContentType.deployments)
    deployment = security_content_builder_deployment.getObject()   

    security_content_builder = SecurityContentDetectionBuilder()
    security_content_builder.setObject(os.path.join(os.path.dirname(__file__), 
        'test_data/detection/valid.yml'), SecurityContentType.detections)
    security_content_builder.addDeployment([deployment], SecurityContentProduct.ESCU)
    detection = security_content_builder.getObject()

    assert detection.deployment.name == "ESCU Default Configuration TTP"  


def test_detection_nes_field_enrichment():
    security_content_builder_deployment = SecurityContentBasicBuilder()
    security_content_builder_deployment.setObject(os.path.join(os.path.dirname(__file__), 
        'test_data/deployment/ESCU/00_default_ttp.yml'), SecurityContentType.deployments)
    deployment = security_content_builder_deployment.getObject()

    security_content_builder = SecurityContentDetectionBuilder()
    security_content_builder.setObject(os.path.join(os.path.dirname(__file__), 
        'test_data/detection/valid.yml'), SecurityContentType.detections)
    security_content_builder.addDeployment([deployment], SecurityContentProduct.ESCU)
    security_content_builder.addNesFields()
    detection = security_content_builder.getObject()

    assert detection.deployment.notable.nes_fields == ['user', 'dest']


def test_detection_annotation_enrichment():
    security_content_builder_deployment = SecurityContentBasicBuilder()
    security_content_builder_deployment.setObject(os.path.join(os.path.dirname(__file__), 
        'test_data/deployment/ESCU/00_default_ttp.yml'), SecurityContentType.deployments)
    deployment = security_content_builder_deployment.getObject()

    security_content_builder = SecurityContentDetectionBuilder()
    security_content_builder.setObject(os.path.join(os.path.dirname(__file__), 
        'test_data/detection/valid.yml'), SecurityContentType.detections)
    security_content_builder.addDeployment([deployment], SecurityContentProduct.ESCU)
    security_content_builder.addAnnotations()
    detection = security_content_builder.getObject()

    valid_annotations = {'mitre_attack': ['T1003.002', 'T1003'], 
        'kill_chain_phases': ['Actions on Objectives'], 
        'cis20': ['CIS 3', 'CIS 5', 'CIS 16'], 
        'nist': ['DE.CM'], 
        'analytic_story': ['Credential Dumping', 'DarkSide Ransomware'], 
        'observable': [{'name': 'user', 'type': 'User', 'role': ['Victim']}, 
            {'name': 'dest', 'type': 'Hostname', 'role': ['Victim']}, 
            {'name': 'parent_process_name', 'type': 'Process', 'role': ['Parent Process']}, 
            {'name': 'process_name', 'type': 'Process', 'role': ['Child Process']}], 
        'context': ['Source:Endpoint', 'Stage:Credential Access'], 
        'impact': 90, 'confidence': 100}
    
    assert detection.annotations == valid_annotations


def test_detection_add_rba():
    security_content_builder = SecurityContentDetectionBuilder()
    security_content_builder.setObject(os.path.join(os.path.dirname(__file__), 
        'test_data/detection/valid.yml'), SecurityContentType.detections)
    security_content_builder.addRBA()
    detection = security_content_builder.getObject()

    valid_risk = [{'risk_object_type': 'user', 'risk_object_field': 'user', 'risk_score': 90}, 
        {'risk_object_type': 'system', 'risk_object_field': 'dest', 'risk_score': 90}, 
        {'threat_object_field': 'parent_process_name', 'threat_object_type': 'process'}, 
        {'threat_object_field': 'process_name', 'threat_object_type': 'process'}]

    assert detection.risk == valid_risk


def test_detection_add_playbooks():
    playbook_builder = SecurityContentBasicBuilder()
    playbook_builder.setObject(os.path.join(os.path.dirname(__file__), 
        'test_data/playbook/example_playbook.yml'), SecurityContentType.playbooks)
    playbook = playbook_builder.getObject()

    security_content_builder = SecurityContentDetectionBuilder()
    security_content_builder.setObject(os.path.join(os.path.dirname(__file__), 
        'test_data/detection/valid.yml'), SecurityContentType.detections)
    security_content_builder.addPlaybook([playbook])
    detection = security_content_builder.getObject()

    assert detection.playbooks[0].name == "Ransomware Investigate and Contain"


def test_detection_enrich_baseline():

    # create own object for baseline with own Builder

    baseline_builder = SecurityContentDetectionBuilder()
    baseline_builder.setObject(os.path.join(os.path.dirname(__file__), 
        'test_data/detection/baseline.yml'), SecurityContentType.detections)
    baseline = baseline_builder.getObject()

    security_content_builder = SecurityContentDetectionBuilder()
    security_content_builder.setObject(os.path.join(os.path.dirname(__file__), 
        'test_data/detection/valid.yml'), SecurityContentType.detections)
    security_content_builder.addBaseline([baseline])
    detection = security_content_builder.getObject()

    assert detection.baselines[0].name == "Previously Seen Users In CloudTrail - Update"