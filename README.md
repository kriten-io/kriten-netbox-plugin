# Kriten NetBox Plugin

The Kriten NetBox Plugin allows control of Kriten deployments (clusters) from NetBox. You can add clusters, runners, tasks and launch jobs from the plugin.

Install Kriten and NetBox(with plugin). Instructions are [here](INSTALL.md).

### Login to Kriten
Open the Kriten swagger page http://kriten-local/swagger/api/index.html

![Login to Kriten](images/kriten-login.png)

### Create an API token

![Create Kriten API token](images/kriten-api-token.png)

![Add Kriten Cluster](images/netbox-add-cluster.png)
In NetBox, go to plugins > Kriten Clusters and add details of the local Kriten cluster.

![Add Kriten Runner](images/netbox-add-runner.png)
This defines where code is stored and container image needed to run it.

![Add Kriten Task](images/netbox-add-task.png)
A task is how to run a program stored in a runner git repository. There may be many tasks per runner depending how the repository is organiised.

![Add Kriten Job](images/netbox-add-job.png)
You are now ready to run a job.

![View Kriten Job](images/netbox-view-job.png)
This job should not take long to run.
