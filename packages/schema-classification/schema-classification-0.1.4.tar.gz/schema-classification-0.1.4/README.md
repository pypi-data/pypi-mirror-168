# schema-classification
This microservice performs the classification of parse results

## Usage
The input format looks like this
```python
input_tokens = [
    {
        "normal": "my",
    },
    {
        "normal": "late",
    },
    {
        "normal": "transport",
    },
    {
        "normal": "late_transport",
        "swaps": {
            "canon": "late_transport",
            "type": "chitchat"
        }
    },
]
```

Calling the service looks like this
```python
from schema_classification import classify

absolute_path = os.path.normpath(
    os.path.join(os.getcwd(), 'resources/testing',
                    'test-intents-0.1.0.yaml'))

svcresult = classify(
    absolute_path=absolute_path,
    input_tokens=input_tokens)
```

The output from this call looks like
```python
{
    'result': [{
        'classification': 'Late_Transport',
        'confidence': 99 }],
    'tokens': {
        'late': '',
        'late_transport': 'chitchat',
        'my': '',
        'transport': ''}
}
```


## Classification via Mapping
Classification of Unstructured Text is a mapping exercise

The mapping is composed of these elements
1. Include One Of
2. Include All Of
3. Exclude One Of
4. Exclude All Of

The classifier will map extracted entities from unstructured text using the listed elements.

for example,

```yaml
TEST_INTENT
  - include_one_of:
    - alpha
    - apple
  - include_all_of:
    - beta
    - gamma
  - exclude_one_of:
    - delta
  - exclude_all_of:
    - epsilon
    - digamma
```

This intent will be selected if the set of extracted entities has either `alpha` or `apple` and has both `(beta, gamma)`. The intent will be discarded if `delta` occurs or if both `(epsilon, digamma)` occur.

In python, everything can be loaded into a native set structure and use native operations like `difference`, `intersection`, `union`, and `symmetric difference`.

Because all set operations are native (underlying C modules), it's extremely fast to find an accurate classification.

The system adds more smarts by figuring out what to do if the rule states `delta` is excluded, and a descendant of `delta` is present.

Or if `alpha` should be included and a sibling or child of `alpha` is present, etc.

In this case, I usually rely on a heuristic to boost or lower confidence and tweak that overtime to get a good result.