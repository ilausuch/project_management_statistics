
# Normalized Model

By utilizing a normalized model for Issue, IssueEvent, and IssueAttribute, we can combine different sources into the same metrics.
This is particularly useful for teams working with different ticket systems and management perspectives. Or for managers to have an overview of the department

- [Issue](#issue)
- [IssueEvent](#issueevent)
- [IssueRelation](#issuerelation)
- [IssueAttribute](#issueattribute)

## Issue

The Issue model contains the common fields expected from a ticket system and provides the last status (and snapshot) of the ticket. These fields include:

Issue basic:
- **issue_id**: A unique identifier for the issue within its specific ticket system.
- **parent_issue_id**: A unique identifier for the parent issue within its specific ticket system.
- **status**: The current status of the issue, such as "open", "in progress", or "closed".
- **type**: The type of issue, such as "bug", "feature", or "task".
- **subject**: A brief description or title of the issue.

Date time fields:
- **created_on**: The date and time when the issue was created.
- **updated_on**: The date and time when the issue was last updated.
- **start_date**: The date and time when work on the issue began (usually is considered that the issue is "in progress" from this point).
- **closed_on**: The date and time when the issue was closed.
- **due_date**: The date and time when the issue is expected to be completed.
- **estimated_hours**: The estimated number of hours required to complete the issue.

Project and context:
- **context**: A string used to filter issues that belong to different groups or contexts. In different ticket systems, this context can vary. 
For example, in the Progress ticket system, the context may be the project, while in Bugzilla, it could be a combination of the product, version, etc.
- **projec**: The name of the project to which the issue belongs.
- **target_version**: The version of the project to which the issue belongs.

Additional fields:
- **assigned_to**: The name of the user to whom the issue is currently assigned.
- **author**: The name of the user who created the issue.
- **priority**: The priority level of the issue, which can help in determining the order of work.
- **tags**: A list of tags associated with the issue.


By storing these fields in the Issue model, you can efficiently filter, sort, and analyze issues from various ticket systems in a consistent format.

### Context
The context_key is designed to help you filter and group issues that belong to different contexts or groups, such as projects, products, or versions.
It is essential to define the context_key in a consistent and meaningful way to make it easy to work with issues from various ticket systems.

To define the context_key, you can follow a standard format, combining relevant context elements and separating them with a delimiter
like a period (.) or a hyphen (-). In the example you provided, the context_key is created by concatenating the product,
version, and an additional numeric identifier:

e.g. product1.version1-4

Here's a step-by-step guide to defining a context_key:

- Identify the relevant context elements for your issue tracking system. For example, in Bugzilla, you may want to include the product and version,
while in the Progress, you might only need the project.
- Choose a consistent delimiter to separate the elements in the context_key. Common delimiters include periods (.), hyphens (-), or underscores (_).
- Combine the context elements using the chosen delimiter to form the context_key.

By consistently defining the context_key in this manner, you can easily filter, sort, and analyze issues that belong to different contexts while 
maintaining compatibility between different ticket systems.

## IssueEvent

The IssueEvent model plays a crucial role in capturing the history of changes that occur to an issue throughout its lifecycle.
By recording these events, you can better understand the evolution of issues, analyze trends, and assess the effectiveness of your team's processes.

The IssueEvent model includes the following fields:

- **issue_id**: A foreign key reference to the associated issue in the Issue model.
- **user_name**: The name of the user who performed the change.
- **created_on**: The date and time when the event occurred.
- **type**: The type of change, such as "status change", "priority change", or "assignment".
- **field**: The field that was modified during the event.
- **old_value**: The previous value of the modified field before the event occurred.
- **new_value**: The updated value of the modified field after the event occurred.

By storing issue events in the IssueEvent model, you can analyze the historical changes and trends for each issue, such as the frequency of status changes,
priority adjustments, or user assignments. This information can help you identify potential areas for improvement, and the effectiveness of your team's processes.
Additionally, maintaining a record of issue events can provide valuable context when exploring and designing new metrics, ensuring that they accurately reflect the desired insights and trends.

## IssueRelation

The IssueRelation model is designed to store the relationships between issues. Each entry in this model includes an issue_id (which links it to the corresponding issue), and a relation_issue_id (which links it to the related issue).

Additianllly, each entry includes a relation_type field, which specifies the type of relationship between the two issues. For example, the relation_type (e.g. "blocks", "duplicates", or "relates to")

The IssueRelation includes the following fields:
- **relation_id**: A unique identifier for the relationship.
- **issue_id**: A foreign key reference to the associated issue in the Issue model.
- **relation_issue_id**: A foreign key reference to the related issue in the Issue model.
- **relation_type**: The type of relationship between the two issues


## IssueAttribute

In addition to the main fields stored in the Issue model, you may encounter other attributes specific to a particular ticket system or relevant to your unique use case.
To accommodate these additional attributes, you can use the IssueAttribute model.

The IssueAttribute model is designed to store key-value pairs associated with an issue. Each entry in this model includes an issue_id (which links it to the corresponding issue),
a key representing the attribute's name, and a value representing the attribute's content.

By storing these additional attributes in the IssueAttribute model, you can capture and preserve valuable information that is not part of the common fields in the Issue model.
This flexible approach allows you to store custom attributes from various ticket systems, enabling more in-depth filtering, analysis, and reporting.

For example, if you encounter a custom attribute called "Version" in one of the ticket systems, you can store it in the IssueAttribute model as follows:

- issue_id: The ID of the issue that has the "Version" attribute.
- key: "Version"
- value: The actual value of the "Version" attribute.

This approach ensures that all relevant data is captured and stored, allowing you to create more accurate and comprehensive metrics and reports.
