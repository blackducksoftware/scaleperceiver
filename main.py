import subprocess
from StringIO import StringIO
import json
import random

image_name = 'gcr.io/gke-verification/blackducksoftware/echoer'


csv = subprocess.Popen(
	"docker image ls --digests {}".format(image_name),
	shell=True,
	stdout=subprocess.PIPE).stdout.read()

def parse_sha(line):
	columns = line.split()
	sha = columns[2][7:]
	return sha

def make_image(line):
	columns = line.split()
	sha = columns[2][7:]
	tag = columns[1]
	return {
#		'ImageName': '{}:{}'.format(image_name, tag),
		'PullSpec': '{}@sha256:{}'.format(image_name, sha),
		'Sha': sha,
		'HubProjectName': '?',
		'HubProjectVersionName': '?',
		'HubScanName': '?'
	}

all_but_first_and_last_lines = csv.split('\n')[1:-1]
shas = map(parse_sha, all_but_first_and_last_lines)
# images = [make_image(line) for line in all_but_first_and_last_lines]

# rows = map(lambda line: line.split()[2], filcsv.split('\n'))
# print '\n'.join(rows)

# print json.dumps(images, indent=2)

def get_random_nums_totalling(total):
	nums = []
	while sum(nums) < total:
		nums.append(random.randint(1, 10))
	return nums

# print get_random_nums_totalling(1000)

def make_scan(sha, project, version, scan):
	return {
		'PullSpec': '{}@sha256:{}'.format(image_name, sha),
		'Sha': sha,
		'HubProjectName': project,
		'HubProjectVersionName': version,
		'HubScanName': scan
	}

# def make_version(version_name):
	

def make_project(name, version_count):
	versions = []
	for i in range(version_count):
		version_name = "test-version-{}".format(i + 1)
		versions.append(make_version(version_name))
	return {
		'Name': name,
		'Versions': versions
	}

def make_projects(total_scans):
	scans = []
	projects = []
	scan_count = 0
	version_counts = get_random_nums_totalling(total_scans)
	for (project_id, version_count) in enumerate(version_counts):
		project = "test-project-{}".format(project_id)
		versions = []
		for version_id in range(version_count):
			scan_index = scan_count % len(shas)
#			print project_id, version_id, scan_count, shas[scan_index]
			version = "proj-{}-version-{}".format(project_id, version_id)
			scan = "proj-{}-version-{}-scan-{}".format(project_id, version_id, scan_count)
			scans.append(make_scan(shas[scan_index], project, version, scan))
			scan_count += 1
			sha = shas[scan_index]
			versions.append({'Name': version, 'Scan': {'Name': scan, 'Sha': sha, 'PullSpec': "{}@sha256:{}".format(image_name, sha)}})
		projects.append({'Name': project, 'Versions': versions})
	return (projects, scans)

print json.dumps(make_projects(25), indent=2)
