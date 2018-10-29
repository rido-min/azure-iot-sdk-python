# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import pytest
from azure.iot.hub.devicesdk.auth.sas_authentication_provider import SharedAccessSignatureAuthenticationProvider


sas_device_token_format = "SharedAccessSignature sr={}&sig={}&se={}"
sas_device_skn_token_format = "SharedAccessSignature sr={}&sig={}&se={}&skn={}"


shared_access_key_name = "alohomora"
hostname = "beauxbatons.academy-net"
device_id = "MyPensieve"
module_id = "Divination"

signature = "IsolemnlySwearThatIamuUptoNogood"
expiry = "1539043658"


def create_sas_token_string_device(is_module=False, is_key_name=False):
    uri = hostname + "/devices/" + device_id
    if is_module:
        uri = uri + "/modules/" + module_id
    if is_key_name:
        return sas_device_skn_token_format.format(uri, signature, expiry, shared_access_key_name)
    else:
        return sas_device_token_format.format(uri, signature, expiry)


def test_all_attributes_for_device():
    sas_string = create_sas_token_string_device()
    sas_auth_provider = SharedAccessSignatureAuthenticationProvider.parse(sas_string)
    assert sas_auth_provider.hostname == hostname
    assert sas_auth_provider.device_id == device_id
    assert hostname in sas_auth_provider.sas_token_str
    assert device_id in sas_auth_provider.sas_token_str


def test_all_attributes_for_module():
    sas_string = create_sas_token_string_device(True)
    sas_auth_provider = SharedAccessSignatureAuthenticationProvider.parse(sas_string)
    assert sas_auth_provider.hostname == hostname
    assert sas_auth_provider.device_id == device_id
    assert hostname in sas_auth_provider.sas_token_str
    assert device_id in sas_auth_provider.sas_token_str
    assert sas_auth_provider.module_id == module_id
    assert hostname in sas_auth_provider.sas_token_str
    assert device_id in sas_auth_provider.sas_token_str
    assert module_id in sas_auth_provider.sas_token_str


def test_device_sastoken_skn():
    sas_string = create_sas_token_string_device(False, True)
    sas_auth_provider = SharedAccessSignatureAuthenticationProvider.parse(sas_string)
    assert sas_auth_provider.hostname == hostname
    assert sas_auth_provider.device_id == device_id
    assert hostname in sas_auth_provider.sas_token_str
    assert device_id in sas_auth_provider.sas_token_str
    assert shared_access_key_name in sas_auth_provider.sas_token_str


def test_raises_auth_provider_created_from_missing_part_shared_access_signature_string():
    with pytest.raises(ValueError, match="The Shared Access Signature must be of the format 'SharedAccessSignature sr=<resource_uri>&sig=<signature>&se=<expiry>' or/and it can additionally contain an optional skn=<keyname> name=value pair."):
        one_part_sas_str = "sr=beauxbatons.academy-net%2Fdevices%2FMyPensieve&sig=IsolemnlySwearThatIamuUptoNogood&se=1539043658&skn=alohomora"
        SharedAccessSignatureAuthenticationProvider.parse(one_part_sas_str)


def test_raises_auth_provider_created_from_shared_access_signature_string_duplicate_keys():
    with pytest.raises(ValueError, match="Invalid Shared Access Signature - Unable to parse"):
        duplicate_sas_str = "SharedAccessSignature sr=beauxbatons.academy-net%2Fdevices%2FMyPensieve&sig=IsolemnlySwearThatIamuUptoNogood&se=1539043658&sr=alohomora"
        SharedAccessSignatureAuthenticationProvider.parse(duplicate_sas_str)


def test_raises_auth_provider_created_from_shared_access_signature_string_bad_keys():
    with pytest.raises(ValueError, match="Invalid keys in Shared Access Signature. The valid keys are sr, sig, se and an optional skn."):
        bad_key_sas_str = "SharedAccessSignature sr=beauxbatons.academy-net%2Fdevices%2FMyPensieve&signature=IsolemnlySwearThatIamuUptoNogood&se=1539043658&skn=alohomora"
        SharedAccessSignatureAuthenticationProvider.parse(bad_key_sas_str)


def test_raises_auth_provider_created_from_incomplete_shared_access_signature_string():
    with pytest.raises(ValueError, match="Invalid Shared Access Signature. It must be of the format 'SharedAccessSignature sr=<resource_uri>&sig=<signature>&se=<expiry>' or/and it can additionally contain an optional skn=<keyname> name=value pair."):
        incomplete_sas_str = "SharedAccessSignature sr=beauxbatons.academy-net%2Fdevices%2FMyPensieve&se=1539043658&skn=alohomora"
        SharedAccessSignatureAuthenticationProvider.parse(incomplete_sas_str)


