## v1.4.0

**feat:** added `--filter_fields` argument to display only specified field(s)

## v1.3.2

**fix:** docker HEALTHCHECK is improved to avoid unhealthy status in swarm cluster  
**feat:** prometheus_client is upgraded to 0.21.0

## v1.3.0

**feat:** add multiple severity options to filter metrics for specify conditions:  
 `--severity INFO PASS WARN`  
 `--severity INFO PASS`


**feat:** main python alpine image is upgraded to `3.12-alpine3.20`  
**feat:** prometheus client library is upgraded to `0.20.0`  
**feat**: readme is updated and small code improvements

## v1.2.1

update `prometheus-client` library to `0.19.0` to avoid following issues:

```
0.19.0 / 2023-11-20 Latest
What's Changed
[FEATURE] support HTTPS/TLS in start_http_server. #946
[BUGFIX] fix: error in determining timestamp less than. #979
```

**Reference:** https://github.com/prometheus/client_python/releases/tag/v0.19.0

## v1.2.0

**feat**: `timebase` starter option is added

```
--timebase second -t N
--timebase minute -t N
--timebase hour -t N (1-24)
```
**feat:** `README` is updated

## v1.1.0

**feat:** add `severity option` to filter benchmark results  
**feat:** `details` column is added in to metric page  
**feat:** argument options are improved  
**feat:** add base health check for docker image

**feat:** updates in readme

* monitoring diagram is added in \_assets
* setup steps are updated for "shell" option

**feat:** following updates were done in base image

* python image upgraded to: `3.12-alpine3.18`
* prometheus library is upgraded to `0.18.0`

## v1.0.0
Initial release of CIS Exporter