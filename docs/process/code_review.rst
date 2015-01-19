.. _code_review:

Code Review
===========

Guidelines for our code review process.

Everyone
********

- Ask for clarification. ("I didn't understand this comment. Can you clarify?")
- Talk in person if there are too many "I didn't understand" comments.

Having Your Code Reviewed
*************************

Before sending a pull request for code review, make sure you have met the :ref:`PR guidelines <pull_requests>`.

- It may be difficult not to perceive code review as personal criticism, but, keep in mind, it is a review of the code, not the person. We can all learn from eachother, and code reviews provide a good environment to do so.
- After addressing all comments from a review, ping your on Flowdock for the next pass.
- If there is a style guideline that affects your PR and you believe the guideline is incorrect, post an issue or send a PR to the `COSDev <https://github.com/CenterForOpenScience/COSDev>`_ repo rather than discussing it in the PR.

Reviewing Code
**************

- Make sure you understand the purpose of the code being reviewed.
- Checkout the branch being reviewed, and manually test the intended behavior.
- In your comments, keep in mind the fact that what you're saying can easily be perceived as personal criticism (even if it's not--it shouldn't be) and adjust your tone accordingly.
- After doing a pass of code review, add a comment with an emoji to signify that your pass is complete and ready to be processed.
- Style fixes should refer to the style guides, when possible.

Example style comment:

.. code-block:: markdown

    > Use parentheses for line continuation.

    From http://cosdev.readthedocs.org/en/latest/style_guides/python.html:
