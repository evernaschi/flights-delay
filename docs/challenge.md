Choosing a model:
In this specific case, both models have the same accuracy (0.55) and similar F1-scores for both classes (0.66 for XGBoost and 0.65 for Logistic Regression). Therefore, there is no clear distinction in terms of performance between these two models with the provided information.

The choice between XGBoost and Logistic Regression should consider factors beyond just the classification report metrics, such as model interpretability, computational efficiency, and ease of implementation.

In those categories, the advantages favor Logistic Regression because it's easier to interpret and makes it more maintainable. Additionally, it is apparently lighter and generally faster to train and predict compared to XGBoost.


Notes:
I had to replace setUp in 'test_model.py' with setUpClass. With setUp, test_model_predict will fail because the model isn't trained. Now, it remains trained from the previous test. It's not an ideal solution, but it's the least disruptive one.
I had to update the 'requirements-test.py' file to use the latest version of the Locust package due to dependency issues and specify 'anyio=3.7.1' to resolve a problem while running the 'api-test'.

Ideas:
Consider using validators or more detailed types to handle requests with invalid values for MES or TIPOVUELO.
Think about adding caching for predictions.