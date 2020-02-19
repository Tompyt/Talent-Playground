apiVersion: v1
kind: Pod
metadata:
  name: air-pod
  namespace: tompyt
  labels:
    svc: air-proxy
    db: discogs
spec:
  containers:
    - name: air-pod
      image: tommy169/air-proxy
      ports:
        - name: mycontainer
          containerPort: 80
          protocol: TCP