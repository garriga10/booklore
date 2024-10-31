build_container_local:
	docker build --no-cache --tag=${IMAGE}:dev .

run_container_local:
	docker run -d -e PORT=8000 -p 8080:8000 ${IMAGE}:dev

build_for_production:
	docker build \
		--platform linux/amd64 \
    -t ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${ARTIFACTSREPO}/${IMAGE}:prod \
		.

push_image_production:
	docker push ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${ARTIFACTSREPO}/${IMAGE}:prod

deploy_to_cloud_run:
	gcloud run deploy \
		--image ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${ARTIFACTSREPO}/${IMAGE}:prod \
		--memory ${MEMORY} \
		--region ${GCP_REGION}

check_logs:
	docker logs -f $(docker ps -q --filter ancestor=${IMAGE}:dev)
