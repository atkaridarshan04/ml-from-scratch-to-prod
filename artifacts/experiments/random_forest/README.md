# Random Forest Artifacts

The trained Random Forest model is not versioned in this repository due to its
large serialized size (~280 MB), which makes it unsuitable for source control
and production deployment.

Random Forest was used as a strong non-linear baseline. Gradient Boosting was
selected as the final production candidate due to better performance and a
significantly smaller artifact size.