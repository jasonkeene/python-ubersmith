#!/usr/bin/env bash

FIXTURE_PATH=tests/fixtures

bin/merge_json.py $FIXTURE_PATH/call_responses.json $FIXTURE_PATH/logged_call_responses.json > $FIXTURE_PATH/merged_call_responses.json
if [ $? -eq 0 ]; then
    rm $FIXTURE_PATH/call_responses.json $FIXTURE_PATH/logged_call_responses.json
    mv $FIXTURE_PATH/merged_call_responses.json $FIXTURE_PATH/call_responses.json
else
    rm $FIXTURE_PATH/merged_call_responses.json
fi
