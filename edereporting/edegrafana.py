"""
Copyright 2022, Institute e-Austria and
    West University of Timsioara, Timisoara, Romania
    https://www.ieat.ro/
    https://www.uvt.ro

Developers:
 * Gabriel Iuhasz, iuhasz.gabriel@info.uvt.ro

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:
    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from grafana_client import GrafanaApi
from edelogger import logger
from datetime import datetime
import time


class EDEGrafanaDash:
    def __init__(self, grafana_token, grafana_url):
        self.dash_dict = {
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": {
          "type": "grafana",
          "uid": "-- Grafana --"
        },
        "enable": True,
        "hide": True,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "target": {
          "limit": 100,
          "matchAny": False,
          "tags": [],
          "type": "dashboard"
        },
        "type": "dashboard"
      }
    ]
  },
  "editable": True,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 0,
  "id": 7,
  "links": [],
  "liveNow": False,
  "panels": [
    {
      "collapsed": False,
      "gridPos": {
        "h": 1,
        "w": 24,
        "x": 0,
        "y": 0
      },
      "id": 66,
      "panels": [],
      "title": "Global",
      "type": "row"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "P1809F7CD0C75ACF3"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": None
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          },
          "unit": "percentunit"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 1
      },
      "id": 68,
      "options": {
        "displayMode": "lcd",
        "minVizHeight": 10,
        "minVizWidth": 0,
        "orientation": "horizontal",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": False
        },
        "showUnfilled": True
      },
      "pluginVersion": "9.2.5",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "editorMode": "code",
          "expr": "avg(1-rate(node_cpu_seconds_total{mode=\"idle\"}[$__rate_interval]))",
          "legendFormat": "__auto",
          "range": True,
          "refId": "A"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "editorMode": "code",
          "expr": "sum(kube_pod_container_resource_limits{resource=\"cpu\"}) / sum(machine_cpu_cores)",
          "hide": False,
          "legendFormat": "__auto",
          "range": True,
          "refId": "B"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "editorMode": "code",
          "expr": "sum(kube_pod_container_resource_requests{resource=\"cpu\"}) / sum(machine_cpu_cores)",
          "hide": False,
          "legendFormat": "__auto",
          "range": True,
          "refId": "C"
        }
      ],
      "title": "Global CPU  Usage",
      "type": "bargauge"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "P1809F7CD0C75ACF3"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "continuous-GrYlRd"
          },
          "custom": {
            "axisCenteredZero": False,
            "axisColorMode": "text",
            "axisLabel": "Memory",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 0,
            "gradientMode": "none",
            "hideFrom": {
              "legend": False,
              "tooltip": False,
              "viz": False
            },
            "lineInterpolation": "smooth",
            "lineWidth": 1,
            "pointSize": 5,
            "scaleDistribution": {
              "type": "linear"
            },
            "showPoints": "never",
            "spanNulls": False,
            "stacking": {
              "group": "A",
              "mode": "none"
            },
            "thresholdsStyle": {
              "mode": "off"
            }
          },
          "displayName": "Cluster Memory",
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": None
              },
              {
                "color": "#EAB839",
                "value": 0.1
              },
              {
                "color": "red",
                "value": 0.8
              }
            ]
          },
          "unit": "percentunit"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 1
      },
      "id": 52,
      "options": {
        "legend": {
          "calcs": [
            "max",
            "min",
            "mean"
          ],
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": True
        },
        "tooltip": {
          "mode": "single",
          "sort": "none"
        }
      },
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "editorMode": "code",
          "expr": "sum(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / sum(node_memory_MemTotal_bytes)",
          "legendFormat": "__auto",
          "range": True,
          "refId": "A"
        }
      ],
      "title": "Cluster Memory Utilization",
      "type": "timeseries"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "P1809F7CD0C75ACF3"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "continuous-GrYlRd"
          },
          "custom": {
            "axisCenteredZero": False,
            "axisColorMode": "text",
            "axisLabel": "CPU %",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 10,
            "gradientMode": "scheme",
            "hideFrom": {
              "legend": False,
              "tooltip": False,
              "viz": False
            },
            "lineInterpolation": "smooth",
            "lineWidth": 2,
            "pointSize": 5,
            "scaleDistribution": {
              "type": "linear"
            },
            "showPoints": "never",
            "spanNulls": False,
            "stacking": {
              "group": "A",
              "mode": "none"
            },
            "thresholdsStyle": {
              "mode": "off"
            }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": None
              },
              {
                "color": "#EAB839",
                "value": 0.5
              },
              {
                "color": "red",
                "value": 0.7
              }
            ]
          },
          "unit": "percentunit"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 9
      },
      "id": 50,
      "options": {
        "legend": {
          "calcs": [],
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": True
        },
        "tooltip": {
          "mode": "single",
          "sort": "none"
        }
      },
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "editorMode": "code",
          "exemplar": True,
          "expr": "avg(1-rate(node_cpu_seconds_total{mode=\"idle\"}[$__rate_interval]))",
          "interval": "",
          "legendFormat": "CPU Usage in %",
          "range": True,
          "refId": "A"
        }
      ],
      "title": "Cluster CPU Utilization",
      "type": "timeseries"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "P1809F7CD0C75ACF3"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "custom": {
            "axisCenteredZero": False,
            "axisColorMode": "text",
            "axisLabel": "Memory",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 25,
            "gradientMode": "opacity",
            "hideFrom": {
              "legend": False,
              "tooltip": False,
              "viz": False
            },
            "lineInterpolation": "smooth",
            "lineWidth": 2,
            "pointSize": 5,
            "scaleDistribution": {
              "type": "linear"
            },
            "showPoints": "never",
            "spanNulls": False,
            "stacking": {
              "group": "A",
              "mode": "none"
            },
            "thresholdsStyle": {
              "mode": "off"
            }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": None
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          },
          "unit": "bytes"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 9
      },
      "id": 60,
      "options": {
        "legend": {
          "calcs": [
            "min",
            "max",
            "mean"
          ],
          "displayMode": "table",
          "placement": "right",
          "showLegend": True
        },
        "tooltip": {
          "mode": "single",
          "sort": "none"
        }
      },
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "editorMode": "code",
          "expr": "sum(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) by (instance)",
          "legendFormat": "__auto",
          "range": True,
          "refId": "A"
        }
      ],
      "title": "Memory Utilization by instance",
      "type": "timeseries"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "P1809F7CD0C75ACF3"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "custom": {
            "axisCenteredZero": False,
            "axisColorMode": "text",
            "axisLabel": "CPU %",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 25,
            "gradientMode": "opacity",
            "hideFrom": {
              "legend": False,
              "tooltip": False,
              "viz": False
            },
            "lineInterpolation": "smooth",
            "lineWidth": 2,
            "pointSize": 5,
            "scaleDistribution": {
              "type": "linear"
            },
            "showPoints": "never",
            "spanNulls": False,
            "stacking": {
              "group": "A",
              "mode": "none"
            },
            "thresholdsStyle": {
              "mode": "off"
            }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": None
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          }
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 17
      },
      "id": 58,
      "options": {
        "legend": {
          "calcs": [
            "min",
            "max",
            "mean"
          ],
          "displayMode": "table",
          "placement": "right",
          "showLegend": True
        },
        "tooltip": {
          "mode": "single",
          "sort": "none"
        }
      },
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "editorMode": "code",
          "expr": "avg(1-rate(node_cpu_seconds_total{mode=\"idle\"}[$__rate_interval])) by (instance)",
          "legendFormat": "__auto",
          "range": True,
          "refId": "A"
        }
      ],
      "title": "CPU Utilization by instance",
      "type": "timeseries"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "P1809F7CD0C75ACF3"
      },
      "description": "Dropped noisy virtual devices for readability.",
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "custom": {
            "axisCenteredZero": False,
            "axisColorMode": "text",
            "axisLabel": "BANDWIDTH",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 25,
            "gradientMode": "opacity",
            "hideFrom": {
              "legend": False,
              "tooltip": False,
              "viz": False
            },
            "lineInterpolation": "smooth",
            "lineWidth": 2,
            "pointSize": 5,
            "scaleDistribution": {
              "type": "linear"
            },
            "showPoints": "never",
            "spanNulls": False,
            "stacking": {
              "group": "A",
              "mode": "none"
            },
            "thresholdsStyle": {
              "mode": "off"
            }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": None
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          },
          "unit": "bytes"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 17
      },
      "id": 62,
      "options": {
        "legend": {
          "calcs": [],
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": False
        },
        "tooltip": {
          "mode": "multi",
          "sort": "none"
        }
      },
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "editorMode": "code",
          "expr": "sum(rate(node_network_receive_bytes_total{device!~\"lxc.*|veth.*\"}[$__rate_interval])) by (device)",
          "legendFormat": "__auto",
          "range": True,
          "refId": "A"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "editorMode": "code",
          "expr": "- sum(rate(node_network_transmit_bytes_total{device!~\"lxc.*|veth.*\"}[$__rate_interval]))  by (device)",
          "hide": False,
          "legendFormat": "__auto",
          "range": True,
          "refId": "B"
        }
      ],
      "title": "Global Network Utilization by device",
      "type": "timeseries"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "P1809F7CD0C75ACF3"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "custom": {
            "axisCenteredZero": False,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 25,
            "gradientMode": "opacity",
            "hideFrom": {
              "legend": False,
              "tooltip": False,
              "viz": False
            },
            "lineInterpolation": "smooth",
            "lineWidth": 2,
            "pointSize": 5,
            "scaleDistribution": {
              "type": "linear"
            },
            "showPoints": "never",
            "spanNulls": False,
            "stacking": {
              "group": "A",
              "mode": "none"
            },
            "thresholdsStyle": {
              "mode": "off"
            }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": None
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          },
          "unit": "bytes"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 25
      },
      "id": 64,
      "options": {
        "legend": {
          "calcs": [],
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": False
        },
        "tooltip": {
          "mode": "single",
          "sort": "none"
        }
      },
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "editorMode": "code",
          "expr": "sum(rate(node_network_receive_bytes_total[$__rate_interval])) by (instance)",
          "legendFormat": "__auto",
          "range": True,
          "refId": "A"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "editorMode": "code",
          "expr": "- sum(rate(node_network_transmit_bytes_total[$__rate_interval])) by (instance)",
          "hide": False,
          "legendFormat": "__auto",
          "range": True,
          "refId": "B"
        }
      ],
      "title": "Total Network Received (with all virtual devices) by instance",
      "type": "timeseries"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "P1809F7CD0C75ACF3"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "custom": {
            "axisCenteredZero": False,
            "axisColorMode": "text",
            "axisLabel": "CPU Cores",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 0,
            "gradientMode": "opacity",
            "hideFrom": {
              "legend": False,
              "tooltip": False,
              "viz": False
            },
            "lineInterpolation": "smooth",
            "lineWidth": 1,
            "pointSize": 5,
            "scaleDistribution": {
              "type": "linear"
            },
            "showPoints": "never",
            "spanNulls": False,
            "stacking": {
              "group": "A",
              "mode": "none"
            },
            "thresholdsStyle": {
              "mode": "off"
            }
          },
          "decimals": 2,
          "mappings": [],
          "max": -1,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": None
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          },
          "unit": "none"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 25
      },
      "id": 54,
      "options": {
        "legend": {
          "calcs": [],
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": True
        },
        "tooltip": {
          "mode": "single",
          "sort": "none"
        }
      },
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "editorMode": "code",
          "expr": "sum(rate(container_cpu_usage_seconds_total{image!=\"\"}[$__rate_interval])) by (namespace)",
          "legendFormat": "__auto",
          "range": True,
          "refId": "A"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "editorMode": "code",
          "expr": "",
          "hide": False,
          "legendFormat": "__auto",
          "range": True,
          "refId": "B"
        }
      ],
      "title": "CPU Utilization by namespace",
      "type": "timeseries"
    },
    {
      "collapsed": True,
      "gridPos": {
        "h": 1,
        "w": 24,
        "x": 0,
        "y": 33
      },
      "id": 20,
      "panels": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "fieldConfig": {
            "defaults": {
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              },
              "unit": "short"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 6,
            "w": 24,
            "x": 0,
            "y": 2
          },
          "id": 12,
          "options": {
            "colorMode": "value",
            "graphMode": "area",
            "justifyMode": "auto",
            "orientation": "auto",
            "reduceOptions": {
              "calcs": [
                "lastNotNull"
              ],
              "fields": "",
              "values": False
            },
            "textMode": "auto"
          },
          "pluginVersion": "9.2.5",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "editorMode": "builder",
              "expr": "kubelet_node_name",
              "legendFormat": "{{node}}",
              "range": True,
              "refId": "A"
            }
          ],
          "title": "Node Names",
          "type": "stat"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "fieldConfig": {
            "defaults": {
              "mappings": [],
              "thresholds": {
                "mode": "percentage",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "orange",
                    "value": 70
                  },
                  {
                    "color": "red",
                    "value": 95
                  }
                ]
              }
            },
            "overrides": []
          },
          "gridPos": {
            "h": 7,
            "w": 24,
            "x": 0,
            "y": 8
          },
          "id": 8,
          "options": {
            "orientation": "auto",
            "reduceOptions": {
              "calcs": [
                "lastNotNull"
              ],
              "fields": "",
              "values": False
            },
            "showThresholdLabels": False,
            "showThresholdMarkers": True
          },
          "pluginVersion": "9.2.5",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "editorMode": "builder",
              "expr": "node_memory_MemFree_bytes",
              "legendFormat": "{{kubernetes_pod_name}}",
              "range": True,
              "refId": "A"
            }
          ],
          "title": "node_memory_memFree_bytes",
          "type": "gauge"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "continuous-GrYlRd"
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              },
              "unit": "bytes"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 0,
            "y": 15
          },
          "id": 10,
          "options": {
            "displayMode": "lcd",
            "minVizHeight": 10,
            "minVizWidth": 0,
            "orientation": "horizontal",
            "reduceOptions": {
              "calcs": [
                "lastNotNull"
              ],
              "fields": "",
              "values": False
            },
            "showUnfilled": True
          },
          "pluginVersion": "9.2.5",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "editorMode": "builder",
              "expr": "node_memory_MemAvailable_bytes",
              "legendFormat": "pod={{kubernetes_pod_name}}, ip={{instance}}",
              "range": True,
              "refId": "A"
            }
          ],
          "title": "Node Memory Available",
          "type": "bargauge"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "thresholds"
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              }
            },
            "overrides": []
          },
          "gridPos": {
            "h": 9,
            "w": 12,
            "x": 12,
            "y": 15
          },
          "id": 2,
          "options": {
            "orientation": "auto",
            "reduceOptions": {
              "calcs": [
                "lastNotNull"
              ],
              "fields": "",
              "values": False
            },
            "showThresholdLabels": False,
            "showThresholdMarkers": True,
            "text": {
              "titleSize": 11
            }
          },
          "pluginVersion": "9.2.5",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "editorMode": "builder",
              "expr": "node_load1",
              "legendFormat": "__auto",
              "range": True,
              "refId": "A"
            }
          ],
          "title": "Node Load CPU 1",
          "type": "gauge"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisCenteredZero": False,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": False,
                  "tooltip": False,
                  "viz": False
                },
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": False,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              }
            },
            "overrides": []
          },
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 0,
            "y": 23
          },
          "id": 4,
          "options": {
            "legend": {
              "calcs": [],
              "displayMode": "list",
              "placement": "bottom",
              "showLegend": True
            },
            "tooltip": {
              "mode": "single",
              "sort": "none"
            }
          },
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "editorMode": "builder",
              "expr": "node_load15",
              "legendFormat": "__auto",
              "range": True,
              "refId": "A"
            }
          ],
          "title": "Node CPU Load 15",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "hideFrom": {
                  "legend": False,
                  "tooltip": False,
                  "viz": False
                }
              },
              "mappings": [],
              "unit": "short"
            },
            "overrides": [
              {
                "__systemRef": "hideSeriesFrom",
                "matcher": {
                  "id": "byNames",
                  "options": {
                    "mode": "exclude",
                    "names": [
                      "master-instance",
                      "worker-instance02",
                      "worker-instance03",
                      "worker-instance01"
                    ],
                    "prefix": "All except:",
                    "readOnly": True
                  }
                },
                "properties": [
                  {
                    "id": "custom.hideFrom",
                    "value": {
                      "legend": True,
                      "tooltip": True,
                      "viz": True
                    }
                  }
                ]
              }
            ]
          },
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 12,
            "y": 24
          },
          "id": 14,
          "options": {
            "displayLabels": [
              "percent"
            ],
            "legend": {
              "displayMode": "list",
              "placement": "right",
              "showLegend": True,
              "values": []
            },
            "pieType": "pie",
            "reduceOptions": {
              "calcs": [
                "lastNotNull"
              ],
              "fields": "",
              "values": False
            },
            "tooltip": {
              "mode": "single",
              "sort": "none"
            }
          },
          "pluginVersion": "9.2.5",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "editorMode": "builder",
              "exemplar": False,
              "expr": "process_cpu_seconds_total",
              "instant": True,
              "legendFormat": "{{instance}}",
              "range": False,
              "refId": "A"
            }
          ],
          "title": "cpu_total_seconds",
          "transformations": [],
          "type": "piechart"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "description": "",
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisCenteredZero": False,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": False,
                  "tooltip": False,
                  "viz": False
                },
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": False,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              }
            },
            "overrides": []
          },
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 0,
            "y": 31
          },
          "id": 18,
          "options": {
            "legend": {
              "calcs": [],
              "displayMode": "list",
              "placement": "bottom",
              "showLegend": True
            },
            "tooltip": {
              "mode": "single",
              "sort": "none"
            }
          },
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "editorMode": "builder",
              "expr": "node_memory_Active_bytes",
              "legendFormat": "__auto",
              "range": True,
              "refId": "A"
            }
          ],
          "title": "Memory Active Bytes",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "fieldConfig": {
            "defaults": {
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              },
              "unit": "short"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 8,
            "w": 24,
            "x": 0,
            "y": 39
          },
          "id": 16,
          "options": {
            "colorMode": "background",
            "graphMode": "none",
            "justifyMode": "auto",
            "orientation": "auto",
            "reduceOptions": {
              "calcs": [
                "lastNotNull"
              ],
              "fields": "",
              "values": False
            },
            "textMode": "auto"
          },
          "pluginVersion": "9.2.5",
          "targets": [
            {
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "editorMode": "builder",
              "exemplar": False,
              "expr": "node_disk_written_bytes_total",
              "instant": True,
              "legendFormat": "pod={{kubernetes_pod_name}}, ip={{instance}}",
              "range": False,
              "refId": "A"
            }
          ],
          "title": "Written Bytes",
          "type": "stat"
        }
      ],
      "title": "Telemetry Overview",
      "type": "row"
    },
    {
      "collapsed": True,
      "gridPos": {
        "h": 1,
        "w": 24,
        "x": 0,
        "y": 34
      },
      "id": 22,
      "panels": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisCenteredZero": False,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 60,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": False,
                  "tooltip": False,
                  "viz": False
                },
                "lineInterpolation": "linear",
                "lineWidth": 2,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "never",
                "spanNulls": False,
                "stacking": {
                  "group": "A",
                  "mode": "normal"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "max": 100,
              "min": 0,
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green",
                    "value": None
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              },
              "unit": "percent"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 7,
            "w": 24,
            "x": 0,
            "y": 3
          },
          "id": 26,
          "links": [],
          "options": {
            "legend": {
              "calcs": [
                "mean",
                "max",
                "min"
              ],
              "displayMode": "table",
              "placement": "right",
              "showLegend": True
            },
            "tooltip": {
              "mode": "multi",
              "sort": "none"
            }
          },
          "pluginVersion": "9.2.5",
          "targets": [
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "sum(rate(node_cpu_seconds_total{$tag=\"$host\"}[$interval])) by (mode) * 100 / count(node_cpu_seconds_total{$tag=\"$host\"}) by (mode) or sum(irate(node_cpu_seconds_total{$tag=\"$host\"}[5m])) by (mode) * 100 / count(node_cpu_seconds_total{$tag=\"$host\"}) by (mode)",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "{{ mode }}",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22sum(rate(node_cpu%7Balias%3D%5C%22%24host%5C%22%7D%5B%24interval%5D))%20by%20(mode)%20*%20100%22%2C%22range_input%22%3A%223600s%22%2C%22end_input%22%3A%222015-10-22%2015%3A27%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "A",
              "step": 2
            }
          ],
          "title": "CPU Usage",
          "type": "timeseries"
        },
        {
          "aliasColors": {},
          "bars": False,
          "dashLength": 10,
          "dashes": False,
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "decimals": 2,
          "editable": True,
          "error": False,
          "fill": 2,
          "fillGradient": 0,
          "grid": {},
          "gridPos": {
            "h": 7,
            "w": 24,
            "x": 0,
            "y": 10
          },
          "hiddenSeries": False,
          "id": 24,
          "legend": {
            "alignAsTable": True,
            "avg": True,
            "current": False,
            "hideEmpty": False,
            "max": True,
            "min": True,
            "rightSide": True,
            "show": True,
            "sortDesc": True,
            "total": False,
            "values": True
          },
          "lines": True,
          "linewidth": 2,
          "links": [],
          "nullPointMode": "null",
          "options": {
            "alertThreshold": True
          },
          "percentage": False,
          "pluginVersion": "9.2.5",
          "pointradius": 5,
          "points": False,
          "renderer": "flot",
          "seriesOverrides": [
            {
              "alias": "Load 1m",
              "color": "#E24D42"
            },
            {
              "alias": "Load 5m",
              "color": "#E0752D"
            },
            {
              "alias": "Load 15m",
              "color": "#E5AC0E"
            }
          ],
          "spaceLength": 10,
          "stack": False,
          "steppedLine": False,
          "targets": [
            {
              "calculatedInterval": "10s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "editorMode": "code",
              "errors": {},
              "expr": "node_load1{$tag=\"$host\"}",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Load 1m",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_load1%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%223601s%22%2C%22end_input%22%3A%222015-10-22%2015%3A27%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3AFalse%2C%22tab%22%3A0%7D%5D",
              "range": True,
              "refId": "A",
              "step": 2,
              "target": ""
            },
            {
              "calculatedInterval": "10s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "node_load5{$tag=\"$host\"}",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Load 5m",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_load5%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%223600s%22%2C%22end_input%22%3A%222015-10-22%2015%3A27%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3AFalse%2C%22tab%22%3A0%7D%5D",
              "refId": "B",
              "step": 2,
              "target": ""
            },
            {
              "calculatedInterval": "10s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "node_load15{$tag=\"$host\"}",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Load 15m",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_load15%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%223600s%22%2C%22end_input%22%3A%222015-10-22%2015%3A27%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3AFalse%2C%22tab%22%3A0%7D%5D",
              "refId": "C",
              "step": 2,
              "target": ""
            }
          ],
          "thresholds": [],
          "timeRegions": [],
          "title": "Load Average",
          "tooltip": {
            "msResolution": False,
            "shared": True,
            "sort": 0,
            "value_type": "individual"
          },
          "type": "graph",
          "xaxis": {
            "mode": "time",
            "show": True,
            "values": []
          },
          "yaxes": [
            {
              "format": "none",
              "label": "",
              "logBase": 1,
              "min": 0,
              "show": True
            },
            {
              "format": "none",
              "logBase": 1,
              "min": 0,
              "show": True
            }
          ],
          "yaxis": {
            "align": False
          }
        },
        {
          "aliasColors": {},
          "bars": False,
          "dashLength": 10,
          "dashes": False,
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "decimals": 2,
          "editable": True,
          "error": False,
          "fill": 2,
          "fillGradient": 0,
          "grid": {},
          "gridPos": {
            "h": 10,
            "w": 24,
            "x": 0,
            "y": 17
          },
          "hiddenSeries": False,
          "id": 48,
          "legend": {
            "alignAsTable": True,
            "avg": True,
            "current": False,
            "hideEmpty": False,
            "max": True,
            "min": True,
            "rightSide": False,
            "show": True,
            "total": False,
            "values": True
          },
          "lines": True,
          "linewidth": 2,
          "links": [],
          "nullPointMode": "null",
          "options": {
            "alertThreshold": True
          },
          "percentage": False,
          "pluginVersion": "9.2.5",
          "pointradius": 5,
          "points": False,
          "renderer": "flot",
          "seriesOverrides": [],
          "spaceLength": 10,
          "stack": False,
          "steppedLine": False,
          "targets": [
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "rate(node_vmstat_pgpgin{$tag=\"$host\"}[$interval]) * 1024 or irate(node_vmstat_pgpgin{$tag=\"$host\"}[5m]) * 1024",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Page In",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemTotal%7Balias%3D%5C%22%24host%5C%22%7D%20-%20(node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D)%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "A",
              "step": 5,
              "target": ""
            },
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "rate(node_vmstat_pgpgout{$tag=\"$host\"}[$interval]) * 1024 or irate(node_vmstat_pgpgout{$tag=\"$host\"}[5m]) * 1024",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Page Out",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "B",
              "step": 5,
              "target": ""
            }
          ],
          "thresholds": [],
          "timeRegions": [],
          "title": "I/O Activity",
          "tooltip": {
            "msResolution": False,
            "shared": True,
            "sort": 0,
            "value_type": "individual"
          },
          "type": "graph",
          "xaxis": {
            "mode": "time",
            "show": True,
            "values": []
          },
          "yaxes": [
            {
              "format": "Bps",
              "label": "",
              "logBase": 1,
              "min": 0,
              "show": True
            },
            {
              "format": "bytes",
              "logBase": 1,
              "min": 0,
              "show": True
            }
          ],
          "yaxis": {
            "align": False
          }
        },
        {
          "aliasColors": {},
          "bars": False,
          "dashLength": 10,
          "dashes": False,
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "decimals": 2,
          "editable": True,
          "error": False,
          "fill": 6,
          "fillGradient": 0,
          "grid": {},
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 0,
            "y": 27
          },
          "height": "",
          "hiddenSeries": False,
          "id": 28,
          "legend": {
            "alignAsTable": True,
            "avg": True,
            "current": False,
            "hideEmpty": False,
            "max": True,
            "min": True,
            "rightSide": False,
            "show": True,
            "total": False,
            "values": True
          },
          "lines": True,
          "linewidth": 2,
          "links": [],
          "nullPointMode": "null",
          "options": {
            "alertThreshold": True
          },
          "percentage": False,
          "pluginVersion": "9.2.5",
          "pointradius": 5,
          "points": False,
          "renderer": "flot",
          "seriesOverrides": [
            {
              "alias": "Used",
              "color": "#0A437C"
            },
            {
              "alias": "Available",
              "color": "#5195CE"
            },
            {
              "alias": "Total",
              "color": "#052B51",
              "legend": False,
              "stack": False
            }
          ],
          "spaceLength": 10,
          "stack": True,
          "steppedLine": False,
          "targets": [
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "node_memory_MemTotal_bytes{$tag$tag=\"$host\"}",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Total",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "C",
              "step": 5,
              "target": ""
            },
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "node_memory_MemTotal_bytes{alias=\"$host\"} - (node_memory_MemAvailable_bytes{$tag=\"$host\"} or (node_memory_MemFree_bytes{$tag=\"$host\"} + node_memory_Buffers_bytes{$tag=\"$host\"} + node_memory_Cached_bytes{$tag=\"$host\"}))",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Used",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemTotal%7Balias%3D%5C%22%24host%5C%22%7D%20-%20(node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D)%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "A",
              "step": 5,
              "target": ""
            },
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "node_memory_MemAvailable_bytes{$tag=\"$host\"} or (node_memory_MemFree_bytes{$tag=\"$host\"} + node_memory_Buffers_bytes{$tag=\"$host\"} + node_memory_Cached_bytes{$tag=\"$host\"})",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Available",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "B",
              "step": 5,
              "target": ""
            }
          ],
          "thresholds": [],
          "timeRegions": [],
          "title": "Memory",
          "tooltip": {
            "msResolution": False,
            "shared": True,
            "sort": 0,
            "value_type": "individual"
          },
          "type": "graph",
          "xaxis": {
            "mode": "time",
            "show": True,
            "values": []
          },
          "yaxes": [
            {
              "format": "bytes",
              "label": "",
              "logBase": 1,
              "min": 0,
              "show": True
            },
            {
              "format": "bytes",
              "logBase": 1,
              "min": 0,
              "show": True
            }
          ],
          "yaxis": {
            "align": False
          }
        },
        {
          "aliasColors": {},
          "bars": False,
          "dashLength": 10,
          "dashes": False,
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "decimals": 2,
          "editable": True,
          "error": False,
          "fill": 6,
          "fillGradient": 0,
          "grid": {},
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 12,
            "y": 27
          },
          "height": "",
          "hiddenSeries": False,
          "id": 30,
          "legend": {
            "alignAsTable": True,
            "avg": True,
            "current": False,
            "hideEmpty": False,
            "max": True,
            "min": True,
            "rightSide": False,
            "show": True,
            "total": False,
            "values": True
          },
          "lines": True,
          "linewidth": 2,
          "links": [],
          "nullPointMode": "null",
          "options": {
            "alertThreshold": True
          },
          "percentage": False,
          "pluginVersion": "9.2.5",
          "pointradius": 5,
          "points": False,
          "renderer": "flot",
          "seriesOverrides": [],
          "spaceLength": 10,
          "stack": True,
          "steppedLine": False,
          "targets": [
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "node_memory_MemTotal_bytes{$tag=\"$host\"} - (node_memory_MemFree_bytes{$tag=\"$host\"} + node_memory_Buffers_bytes{$tag=\"$host\"} + node_memory_Cached_bytes{$tag=\"$host\"})",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Used",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemTotal%7Balias%3D%5C%22%24host%5C%22%7D%20-%20(node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D)%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "A",
              "step": 5,
              "target": ""
            },
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "node_memory_MemFree_bytes{$tag=\"$host\"}",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Free",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "B",
              "step": 5,
              "target": ""
            },
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "node_memory_Buffers_bytes{$tag=\"$host\"}",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Buffers",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "D",
              "step": 5,
              "target": ""
            },
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "node_memory_Cached_bytes{$tag=\"$host\"}",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Cached",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "E",
              "step": 5,
              "target": ""
            }
          ],
          "thresholds": [],
          "timeRegions": [],
          "title": "Memory Distribution",
          "tooltip": {
            "msResolution": False,
            "shared": True,
            "sort": 0,
            "value_type": "individual"
          },
          "type": "graph",
          "xaxis": {
            "mode": "time",
            "show": True,
            "values": []
          },
          "yaxes": [
            {
              "format": "bytes",
              "label": "",
              "logBase": 1,
              "min": 0,
              "show": True
            },
            {
              "format": "bytes",
              "logBase": 1,
              "min": 0,
              "show": True
            }
          ],
          "yaxis": {
            "align": False
          }
        },
        {
          "aliasColors": {},
          "bars": False,
          "dashLength": 10,
          "dashes": False,
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "decimals": 2,
          "editable": True,
          "error": False,
          "fill": 6,
          "fillGradient": 0,
          "grid": {},
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 0,
            "y": 35
          },
          "hiddenSeries": False,
          "id": 40,
          "legend": {
            "alignAsTable": True,
            "avg": True,
            "current": False,
            "hideEmpty": False,
            "max": True,
            "min": True,
            "rightSide": False,
            "show": True,
            "total": False,
            "values": True
          },
          "lines": True,
          "linewidth": 2,
          "links": [],
          "nullPointMode": "null",
          "options": {
            "alertThreshold": True
          },
          "percentage": False,
          "pluginVersion": "9.2.5",
          "pointradius": 5,
          "points": False,
          "renderer": "flot",
          "seriesOverrides": [],
          "spaceLength": 10,
          "stack": True,
          "steppedLine": False,
          "targets": [
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "rate(node_network_receive_bytes_total{$tag=\"$host\", device!=\"lo\"}[$interval]) or irate(node_network_receive_bytes_total{$tag=\"$host\", device!=\"lo\"}[5m])",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Inbound: {{ device }}",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "B",
              "step": 5,
              "target": ""
            },
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "rate(node_network_transmit_bytes_total{$tag=\"$host\", device!=\"lo\"}[$interval]) or irate(node_network_transmit_bytes_total{$tag=\"$host\", device!=\"lo\"}[5m])",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Outbound: {{ device }}",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemTotal%7Balias%3D%5C%22%24host%5C%22%7D%20-%20(node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D)%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "A",
              "step": 5,
              "target": ""
            }
          ],
          "thresholds": [],
          "timeRegions": [],
          "title": "Network Traffic",
          "tooltip": {
            "msResolution": False,
            "shared": True,
            "sort": 0,
            "value_type": "individual"
          },
          "type": "graph",
          "xaxis": {
            "mode": "time",
            "show": True,
            "values": []
          },
          "yaxes": [
            {
              "format": "Bps",
              "label": "",
              "logBase": 1,
              "min": 0,
              "show": True
            },
            {
              "format": "bytes",
              "logBase": 1,
              "min": 0,
              "show": True
            }
          ],
          "yaxis": {
            "align": False
          }
        },
        {
          "aliasColors": {},
          "bars": True,
          "dashLength": 10,
          "dashes": False,
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "decimals": 2,
          "editable": True,
          "error": False,
          "fill": 6,
          "fillGradient": 0,
          "grid": {},
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 12,
            "y": 35
          },
          "hiddenSeries": False,
          "id": 42,
          "legend": {
            "alignAsTable": True,
            "avg": True,
            "current": False,
            "hideEmpty": False,
            "max": True,
            "min": True,
            "rightSide": False,
            "show": True,
            "sort": "min",
            "sortDesc": True,
            "total": False,
            "values": True
          },
          "lines": False,
          "linewidth": 2,
          "links": [],
          "nullPointMode": "null",
          "options": {
            "alertThreshold": True
          },
          "percentage": False,
          "pluginVersion": "9.2.5",
          "pointradius": 5,
          "points": False,
          "renderer": "flot",
          "seriesOverrides": [],
          "spaceLength": 10,
          "stack": True,
          "steppedLine": False,
          "targets": [
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "sum(increase(node_network_receive_bytes{$tag=\"$host\", device!=\"lo\"}[1h]))",
              "format": "time_series",
              "interval": "1h",
              "intervalFactor": 1,
              "legendFormat": "Received",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemTotal%7Balias%3D%5C%22%24host%5C%22%7D%20-%20(node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D)%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "A",
              "step": 3600,
              "target": ""
            },
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "sum(increase(node_network_transmit_bytes{$tag=\"$host\", device!=\"lo\"}[1h]))",
              "format": "time_series",
              "interval": "1h",
              "intervalFactor": 1,
              "legendFormat": "Sent",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemTotal%7Balias%3D%5C%22%24host%5C%22%7D%20-%20(node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D)%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "B",
              "step": 3600,
              "target": ""
            }
          ],
          "thresholds": [],
          "timeFrom": "24h",
          "timeRegions": [],
          "title": "Network Utilization Hourly",
          "tooltip": {
            "msResolution": False,
            "shared": True,
            "sort": 0,
            "value_type": "individual"
          },
          "type": "graph",
          "xaxis": {
            "mode": "time",
            "show": True,
            "values": []
          },
          "yaxes": [
            {
              "format": "bytes",
              "label": "",
              "logBase": 1,
              "min": 0,
              "show": True
            },
            {
              "format": "bytes",
              "logBase": 1,
              "min": 0,
              "show": True
            }
          ],
          "yaxis": {
            "align": False
          }
        },
        {
          "aliasColors": {},
          "bars": False,
          "dashLength": 10,
          "dashes": False,
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "decimals": 2,
          "editable": True,
          "error": False,
          "fill": 2,
          "fillGradient": 0,
          "grid": {},
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 0,
            "y": 43
          },
          "hiddenSeries": False,
          "id": 46,
          "legend": {
            "alignAsTable": True,
            "avg": True,
            "current": False,
            "hideEmpty": False,
            "max": True,
            "min": True,
            "rightSide": False,
            "show": True,
            "total": False,
            "values": True
          },
          "lines": True,
          "linewidth": 2,
          "links": [],
          "nullPointMode": "null",
          "options": {
            "alertThreshold": True
          },
          "percentage": False,
          "pluginVersion": "9.2.5",
          "pointradius": 5,
          "points": False,
          "renderer": "flot",
          "seriesOverrides": [],
          "spaceLength": 10,
          "stack": False,
          "steppedLine": False,
          "targets": [
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "rate(node_vmstat_pswpin{$tag=\"$host\"}[$interval]) * 4096 or irate(node_vmstat_pswpin{$tag=\"$host\"}[5m]) * 4096",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Swap In",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemTotal%7Balias%3D%5C%22%24host%5C%22%7D%20-%20(node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D)%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "A",
              "step": 5,
              "target": ""
            },
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "rate(node_vmstat_pswpout{$tag=\"$host\"}[$interval]) * 4096 or irate(node_vmstat_pswpout{$tag=\"$host\"}[5m]) * 4096",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Swap Out",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "B",
              "step": 5,
              "target": ""
            }
          ],
          "thresholds": [],
          "timeRegions": [],
          "title": "Swap Activity",
          "tooltip": {
            "msResolution": False,
            "shared": True,
            "sort": 0,
            "value_type": "individual"
          },
          "type": "graph",
          "xaxis": {
            "mode": "time",
            "show": True,
            "values": []
          },
          "yaxes": [
            {
              "format": "Bps",
              "label": "",
              "logBase": 1,
              "min": 0,
              "show": True
            },
            {
              "format": "bytes",
              "logBase": 1,
              "min": 0,
              "show": True
            }
          ],
          "yaxis": {
            "align": False
          }
        },
        {
          "aliasColors": {},
          "bars": False,
          "dashLength": 10,
          "dashes": False,
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "decimals": 2,
          "editable": True,
          "error": False,
          "fill": 6,
          "fillGradient": 0,
          "grid": {},
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 12,
            "y": 43
          },
          "hiddenSeries": False,
          "id": 44,
          "legend": {
            "alignAsTable": True,
            "avg": True,
            "current": False,
            "hideEmpty": False,
            "max": True,
            "min": True,
            "rightSide": False,
            "show": True,
            "total": False,
            "values": True
          },
          "lines": True,
          "linewidth": 2,
          "links": [],
          "nullPointMode": "null",
          "options": {
            "alertThreshold": True
          },
          "percentage": False,
          "pluginVersion": "9.2.5",
          "pointradius": 5,
          "points": False,
          "renderer": "flot",
          "seriesOverrides": [
            {
              "alias": "Used",
              "color": "#584477"
            },
            {
              "alias": "Free",
              "color": "#AEA2E0"
            }
          ],
          "spaceLength": 10,
          "stack": True,
          "steppedLine": False,
          "targets": [
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "node_memory_SwapTotal_bytes{$tag=\"$host\"} - node_memory_SwapFree_bytes{$tag=\"$host\"}",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Used",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemTotal%7Balias%3D%5C%22%24host%5C%22%7D%20-%20(node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D)%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "A",
              "step": 5,
              "target": ""
            },
            {
              "calculatedInterval": "2s",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "node_memory_SwapFree_bytes{$tag=\"$host\"}",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Free",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_memory_MemFree%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Buffers%7Balias%3D%5C%22%24host%5C%22%7D%20%2B%20node_memory_Cached%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%22900s%22%2C%22end_input%22%3A%222015-10-22%2015%3A25%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "B",
              "step": 5,
              "target": ""
            }
          ],
          "thresholds": [],
          "timeRegions": [],
          "title": "Swap",
          "tooltip": {
            "msResolution": False,
            "shared": True,
            "sort": 0,
            "value_type": "individual"
          },
          "type": "graph",
          "xaxis": {
            "mode": "time",
            "show": True,
            "values": []
          },
          "yaxes": [
            {
              "format": "bytes",
              "label": "",
              "logBase": 1,
              "min": 0,
              "show": True
            },
            {
              "format": "bytes",
              "logBase": 1,
              "min": 0,
              "show": True
            }
          ],
          "yaxis": {
            "align": False
          }
        },
        {
          "aliasColors": {},
          "bars": False,
          "dashLength": 10,
          "dashes": False,
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "decimals": 2,
          "editable": True,
          "error": False,
          "fill": 2,
          "fillGradient": 0,
          "grid": {},
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 0,
            "y": 51
          },
          "hiddenSeries": False,
          "id": 38,
          "legend": {
            "alignAsTable": True,
            "avg": True,
            "current": False,
            "hideEmpty": False,
            "max": True,
            "min": True,
            "rightSide": False,
            "show": True,
            "total": False,
            "values": True
          },
          "lines": True,
          "linewidth": 2,
          "links": [],
          "nullPointMode": "null",
          "options": {
            "alertThreshold": True
          },
          "percentage": False,
          "pluginVersion": "9.2.5",
          "pointradius": 5,
          "points": False,
          "renderer": "flot",
          "seriesOverrides": [
            {
              "alias": "Interrupts",
              "color": "#D683CE"
            }
          ],
          "spaceLength": 10,
          "stack": False,
          "steppedLine": False,
          "targets": [
            {
              "calculatedInterval": "2m",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "rate(node_intr_total{$tag=\"$host\"}[$interval]) or irate(node_intr_total{$tag=\"$host\"}[5m])",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Interrupts",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_procs_running%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%2243200s%22%2C%22end_input%22%3A%222015-9-18%2013%3A46%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "A",
              "step": 5,
              "target": ""
            }
          ],
          "thresholds": [],
          "timeRegions": [],
          "title": "Interrupts",
          "tooltip": {
            "msResolution": True,
            "shared": True,
            "sort": 0,
            "value_type": "individual"
          },
          "type": "graph",
          "xaxis": {
            "mode": "time",
            "show": True,
            "values": []
          },
          "yaxes": [
            {
              "format": "none",
              "label": "",
              "logBase": 1,
              "min": 0,
              "show": True
            },
            {
              "format": "none",
              "logBase": 1,
              "min": 0,
              "show": True
            }
          ],
          "yaxis": {
            "align": False
          }
        },
        {
          "aliasColors": {},
          "bars": False,
          "dashLength": 10,
          "dashes": False,
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "decimals": 2,
          "editable": True,
          "error": False,
          "fill": 2,
          "fillGradient": 0,
          "grid": {},
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 12,
            "y": 51
          },
          "hiddenSeries": False,
          "id": 36,
          "legend": {
            "alignAsTable": True,
            "avg": True,
            "current": False,
            "hideEmpty": False,
            "max": True,
            "min": True,
            "rightSide": False,
            "show": True,
            "total": False,
            "values": True
          },
          "lines": True,
          "linewidth": 2,
          "links": [],
          "nullPointMode": "null",
          "options": {
            "alertThreshold": True
          },
          "percentage": False,
          "pluginVersion": "9.2.5",
          "pointradius": 5,
          "points": False,
          "renderer": "flot",
          "seriesOverrides": [],
          "spaceLength": 10,
          "stack": False,
          "steppedLine": False,
          "targets": [
            {
              "calculatedInterval": "2m",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "rate(node_context_switches_total{$tag=\"$host\"}[$interval]) or irate(node_context_switches_total{$tag=\"$host\"}[5m])",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Context Switches",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_procs_running%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%2243200s%22%2C%22end_input%22%3A%222015-9-18%2013%3A46%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "A",
              "step": 5,
              "target": ""
            }
          ],
          "thresholds": [],
          "timeRegions": [],
          "title": "Context Switches",
          "tooltip": {
            "msResolution": False,
            "shared": True,
            "sort": 0,
            "value_type": "individual"
          },
          "type": "graph",
          "xaxis": {
            "mode": "time",
            "show": True,
            "values": []
          },
          "yaxes": [
            {
              "format": "none",
              "label": "",
              "logBase": 1,
              "min": 0,
              "show": True
            },
            {
              "format": "none",
              "logBase": 1,
              "min": 0,
              "show": True
            }
          ],
          "yaxis": {
            "align": False
          }
        },
        {
          "aliasColors": {},
          "bars": True,
          "dashLength": 10,
          "dashes": False,
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "decimals": 2,
          "editable": True,
          "error": False,
          "fill": 2,
          "fillGradient": 0,
          "grid": {},
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 0,
            "y": 59
          },
          "hiddenSeries": False,
          "id": 34,
          "legend": {
            "alignAsTable": True,
            "avg": True,
            "current": False,
            "hideEmpty": False,
            "max": True,
            "min": True,
            "rightSide": False,
            "show": True,
            "total": False,
            "values": True
          },
          "lines": False,
          "linewidth": 2,
          "links": [],
          "nullPointMode": "null",
          "options": {
            "alertThreshold": True
          },
          "percentage": False,
          "pluginVersion": "9.2.5",
          "pointradius": 5,
          "points": False,
          "renderer": "flot",
          "seriesOverrides": [
            {
              "alias": "Processes blocked waiting for I/O to complete",
              "color": "#E24D42"
            },
            {
              "alias": "Processes in runnable state",
              "color": "#6ED0E0"
            }
          ],
          "spaceLength": 10,
          "stack": True,
          "steppedLine": False,
          "targets": [
            {
              "calculatedInterval": "2m",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "node_procs_running{$tag=\"$host\"}",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Processes in runnable state",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_procs_running%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%2243200s%22%2C%22end_input%22%3A%222015-9-18%2013%3A46%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "A",
              "step": 5,
              "target": ""
            },
            {
              "calculatedInterval": "2m",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "node_procs_blocked{$tag=\"$host\"}",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Processes blocked waiting for I/O to complete",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_procs_blocked%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%2243200s%22%2C%22end_input%22%3A%222015-9-18%2013%3A46%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "B",
              "step": 5,
              "target": ""
            }
          ],
          "thresholds": [],
          "timeRegions": [],
          "title": "Processes",
          "tooltip": {
            "msResolution": False,
            "shared": True,
            "sort": 0,
            "value_type": "individual"
          },
          "type": "graph",
          "xaxis": {
            "mode": "time",
            "show": True,
            "values": []
          },
          "yaxes": [
            {
              "format": "none",
              "label": "",
              "logBase": 1,
              "min": 0,
              "show": True
            },
            {
              "format": "none",
              "logBase": 1,
              "min": 0,
              "show": True
            }
          ],
          "yaxis": {
            "align": False
          }
        },
        {
          "aliasColors": {},
          "bars": True,
          "dashLength": 10,
          "dashes": False,
          "datasource": {
            "type": "prometheus",
            "uid": "P1809F7CD0C75ACF3"
          },
          "decimals": 2,
          "editable": True,
          "error": False,
          "fill": 2,
          "fillGradient": 0,
          "grid": {},
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 12,
            "y": 59
          },
          "hiddenSeries": False,
          "id": 32,
          "legend": {
            "alignAsTable": True,
            "avg": True,
            "current": False,
            "hideEmpty": False,
            "max": True,
            "min": True,
            "rightSide": False,
            "show": True,
            "total": False,
            "values": True
          },
          "lines": False,
          "linewidth": 2,
          "links": [],
          "nullPointMode": "null",
          "options": {
            "alertThreshold": True
          },
          "percentage": False,
          "pluginVersion": "9.2.5",
          "pointradius": 5,
          "points": False,
          "renderer": "flot",
          "seriesOverrides": [
            {
              "alias": "Forks",
              "color": "#EF843C"
            }
          ],
          "spaceLength": 10,
          "stack": False,
          "steppedLine": False,
          "targets": [
            {
              "calculatedInterval": "2m",
              "datasource": {
                "type": "prometheus",
                "uid": "P1809F7CD0C75ACF3"
              },
              "datasourceErrors": {},
              "errors": {},
              "expr": "rate(node_forks_total{$tag=\"$host\"}[$interval]) or irate(node_forks_total{$tag=\"$host\"}[5m])",
              "format": "time_series",
              "intervalFactor": 1,
              "legendFormat": "Forks",
              "metric": "",
              "prometheusLink": "/api/datasources/proxy/1/graph#%5B%7B%22expr%22%3A%22node_procs_running%7Balias%3D%5C%22%24host%5C%22%7D%22%2C%22range_input%22%3A%2243200s%22%2C%22end_input%22%3A%222015-9-18%2013%3A46%22%2C%22step_input%22%3A%22%22%2C%22stacked%22%3ATrue%2C%22tab%22%3A0%7D%5D",
              "refId": "A",
              "step": 5,
              "target": ""
            }
          ],
          "thresholds": [],
          "timeRegions": [],
          "title": "Forks",
          "tooltip": {
            "msResolution": False,
            "shared": True,
            "sort": 0,
            "value_type": "individual"
          },
          "type": "graph",
          "xaxis": {
            "mode": "time",
            "show": True,
            "values": []
          },
          "yaxes": [
            {
              "format": "none",
              "label": "",
              "logBase": 1,
              "min": 0,
              "show": True
            },
            {
              "format": "none",
              "logBase": 1,
              "min": 0,
              "show": True
            }
          ],
          "yaxis": {
            "align": False
          }
        }
      ],
      "title": "Telemetry System",
      "type": "row"
    }
  ],
  "refresh": False,
  "schemaVersion": 37,
  "style": "dark",
  "tags": [
    "ede_test"
  ],
  "templating": {
    "list": [
      {
        "auto": True,
        "auto_count": 30,
        "auto_min": "1s",
        "current": {
          "selected": False,
          "text": "1s",
          "value": "1s"
        },
        "hide": 0,
        "label": "interval",
        "name": "interval",
        "options": [
          {
            "selected": False,
            "text": "auto",
            "value": "$__auto_interval_interval"
          },
          {
            "selected": True,
            "text": "1s",
            "value": "1s"
          },
          {
            "selected": False,
            "text": "5s",
            "value": "5s"
          },
          {
            "selected": False,
            "text": "1m",
            "value": "1m"
          },
          {
            "selected": False,
            "text": "5m",
            "value": "5m"
          },
          {
            "selected": False,
            "text": "1h",
            "value": "1h"
          },
          {
            "selected": False,
            "text": "6h",
            "value": "6h"
          },
          {
            "selected": False,
            "text": "1d",
            "value": "1d"
          }
        ],
        "query": "1s,5s,1m,5m,1h,6h,1d",
        "queryValue": "",
        "refresh": 2,
        "skipUrlSync": False,
        "type": "interval"
      },
      {
        "current": {
          "isNone": True,
          "selected": False,
          "text": "None",
          "value": ""
        },
        "datasource": {
          "type": "prometheus",
          "uid": "P1809F7CD0C75ACF3"
        },
        "definition": "label_values($tag)",
        "hide": 0,
        "includeAll": False,
        "label": "Host",
        "multi": False,
        "name": "host",
        "options": [],
        "query": {
          "query": "label_values($tag)",
          "refId": "StandardVariableQuery"
        },
        "refresh": 1,
        "regex": "",
        "skipUrlSync": False,
        "sort": 0,
        "type": "query"
      },
      {
        "current": {
          "selected": True,
          "text": "alias",
          "value": "alias"
        },
        "hide": 0,
        "includeAll": False,
        "multi": False,
        "name": "tag",
        "options": [
          {
            "selected": False,
            "text": "instance",
            "value": "instance"
          },
          {
            "selected": True,
            "text": "alias",
            "value": "alias"
          }
        ],
        "query": "instance, alias",
        "queryValue": "",
        "skipUrlSync": False,
        "type": "custom"
      },
      {
        "current": {
          "selected": True,
          "text": [
            "All"
          ],
          "value": [
            "$__all"
          ]
        },
        "datasource": {
          "type": "prometheus",
          "uid": "P1809F7CD0C75ACF3"
        },
        "definition": "label_values(kube_pod_info, namespace)",
        "hide": 0,
        "includeAll": True,
        "multi": True,
        "name": "namespace",
        "options": [],
        "query": {
          "query": "label_values(kube_pod_info, namespace)",
          "refId": "StandardVariableQuery"
        },
        "refresh": 1,
        "regex": "",
        "skipUrlSync": False,
        "sort": 1,
        "type": "query"
      }
    ]
  },
  "time": {
    "from": "2023-10-10T08:21:34.502Z",
    "to": "2023-10-10T11:13:27.002Z"
  },
  "timepicker": {},
  "timezone": "",
  "title": "EDE",
  "uid": "4nVE5qmIz",
  "version": 29,
  "weekStart": ""
}
        self.grafana_token = grafana_token
        self.grafana_url = grafana_url
        self. grafana = GrafanaApi.from_url(url=self.grafana_url, credential=self.grafana_token)
        self.dash_uid = None
        self.dash_url = None
        self.dash_id = None

    def get_dash(self, tag, working_dash=False):
        """
        gets dash information based on tag.
        :param tag: Tag to search for.
        :param working_dash: If dashboard is found and working_dash set to true it will be set as the current working dash
        :return: Dash UID, Dash URL, Dash ID
        """
        dashboards = self.grafana.search.search_dashboards(tag=tag)

        if not dashboards:
            logger.error('[{}] : [ERROR] No Grafana dashes found with tag: {}'.format(
              datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), tag))
            return 0, 0, 0
        dash_uid = dashboards[0]['uid']
        if len(dashboards) > 1:  # Check if more than one dash has the same tag and select the first one
            logger.warning('[{}] : [WARN] More then one dashboard found with the tag, selecting first dash with uid: {}'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), dash_uid))
        dash_url = dashboards[0]['url']
        dash_id = dashboards[0]['id']
        logger.info(
            '[{}] : [INFO] Dashboard found with uid {} and url {} for tag {}'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), dash_uid, dash_url, tag))
        if working_dash:
            self.dash_uid = dash_uid
            self.dash_url = dash_url
            self.dash_id = dash_id
        return dash_uid, dash_url, dash_id

    def generate_dash(self,
                      tag,
                      title="UVT Serrano dash",
                      timezone='browser',
                      refresh='10s',
                      dtime={'from': 'now-6h',
                            'to': 'now'}
                      ):
        """
        Generates dash descriptor
        :param tag: Tag to be used for dashboard
        :param title: Title of Dashboard
        :param timezone: Timezone to be used for
        :param refresh: Refresh rate
        :param dtime: Time interval to be shown by default
        :return:  Dash descriptor dictionary
        """
        dash_inf = self.get_dash(tag=tag, working_dash=False)
        if not dash_inf[1]:
            self.dash_dict['dashboard']['title'] = title
            self.dash_dict['dashboard']['timezone'] = timezone
            self.dash_dict['dashboard']['refresh'] = refresh
            self.dash_dict['dashboard']['time'] = dtime
            self.dash_dict['dashboard']['tags'] = [tag]  # TODO add support for more than one tag

            logger.warning(
              '[{}] : [WARN] No dash found with tag {} creating ...'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), tag))

        else:
            logger.warning(
              '[{}] : [WARN] Dash found with uid {} and url {} skipping generation of new dash'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), dash_inf[0], dash_inf[1]))
            return 0  # TODO enable override of existing dash
        return self.dash_dict

    def create_dash(self):
        """
        Creates dashboad based on dash JSON Descriptor
        :return:  dashboard UID, URL, ID
        """
        try:
            dash_inf = self.grafana.dashboard.update_dashboard(dashboard=self.dash_dict)
            self.dash_uid = dash_inf['uid']
            self.dash_url = dash_inf['url']
            self.dash_id = dash_inf['id']
            logger.info(
              '[{}] : [INFO] Created new dashboard with id {}, url {} and tag {}'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                self.dash_id, self.dash_url, "test_dash"))  # Todo default tag is set in template
        except Exception as inst:
            logger.error('[{}] : [ERROR] Failed to create dashboard with {} and {}'.format(
              datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), type(inst), inst.args))
            return 0
        return dash_inf

    def delete_dash(self, uid=None):
        """
        Deletes dashboard based on uid
        :param uid: UID of dashboard to b deleted, if not set the default dashboard will be deleted
        """
        dashboard_uid = 0
        try:
            if uid:
                dashboard_uid = uid
            else:
                dashboard_uid = self.dash_uid
            self.grafana.dashboard.delete_dashboard(dashboard_uid=dashboard_uid)
            logger.info(
              '[{}] : [INFO] Dashboard with uid {} deleted'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), dashboard_uid))
        except Exception as inst:
            logger.error(
              '[{}] : [ERROR] Failed deleting dashboard with uid {} with {} and {}'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), dashboard_uid,
                type(inst), inst.args))

    def push_annotation(self, time_from, time_to, anomaly_tags, message, dash_id=None):
        """
        Pushes annotations to grafana
        :param time_from: Start of annotation in utc
        :param time_to: End of annotation in utc
        :param anomaly_tags: Tag for the anomaly to be used
        :param message: Message when creating anomaly
        :param dash_id: ID of the dash where annotations are to be pushed
        :return: annotation descriptor
        """
        if self.dash_id is not None:
            logger.info('[{}] : [INFO] Dash id initialized to {}'.format(
              datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), self.dash_id))
            l_dash_id = self.dash_id
        elif dash_id is not None:
            logger.info('[{}] : [DEBUG] Dash id set to {}'.format(
              datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), dash_id))
            l_dash_id = dash_id
        else:
            logger.error('[{}] : [ERROR] Dash id not initialized or provided'.format(
              datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
            return 0

        try:
            annotation = self.grafana.annotations.add_annotation(dashboard_id=l_dash_id,
                                                                 time_from=time_from,
                                                                 time_to=time_to,
                                                                 tags=anomaly_tags,
                                                                 text=message)
            logger.info(
              '[{}] : [DEBUG] Detected annotations {}'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), len(annotation)))
        except Exception as inst:
            logger.error('[{}] : [ERROR] "Failed to push annomalies with {} and {}'.format(
              datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), type(inst), inst.args))
            return 0
        return annotation

    def get_annotations(self,
                        time_from=None,
                        time_to=None,
                        alert_id=None,
                        dash_id=None,
                        panel_id=None,
                        user_id=None,
                        ann_type=None,
                        tags=None,
                        limit=None):
        """
        Wrapper for get_annotation method from grafana_client.

        :param time_from: Start of query period
        :param time_to:  End of query period
        :param alert_id: Alert ID
        :param dash_id: Dasboard ID
        :param panel_id: Panel ID
        :param user_id: User ID
        :param ann_type: Annotation type
        :param tags: Tags used
        :param limit: Limit
        :return: List of annotation descriptors
        """
        try:
            annotations = self.grafana.annotations.get_annotation(
              time_from=time_from,
              time_to=time_to,
              alert_id=alert_id,
              dashboard_id=dash_id,
              panel_id=panel_id,
              user_id=user_id,
              ann_type=ann_type,
              tags=tags,
              limit=limit)
        except Exception as inst:
            logger.error(
              '[{}] : [ERROR] Failed fetching annotations with {} and {}'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), type(inst), inst.args))
            return 0
        return annotations

    def delete_annotation(self, annotations):
        """
        Delete Annotations

        :param annotations: list of annotation descritors
        """
        try:
            for annotation in annotations:
                annotation_id = annotation['id']
                self.grafana.annotations.delete_annotations_by_id(annotations_id=annotation_id)
                logger.info(
                  '[{}] : [INFO] Deleting annotation with id {}, dashboard id {}'.format(
                    datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), annotation_id, annotation['dashboardId']))
        except Exception as inst:
            logger.error('[{}] : [ERROR] Failed to delete annotation with {} and {}'.format(
              datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), type(inst), inst.args))
            return 0
        return 1


if __name__ == "__main__":

    # Test Credentials
    url = "https://grafana.monitoring.services.cloud.ict-serrano.eu"
    credential = "eyJrIjoiOG00bERhdWJ5Q0JVY3JWOTNSNzM4bGpXS2ZmU3Vsa2MiLCJuIjoic2VycmFub19ncmFmYW5hX2FwaV9rZXkiLCJpZCI6MX0="

    test = EDEGrafanaDash(grafana_token=credential, grafana_url=url)

    # print(test.get_dash(tag="test_tag"))

    print(test.generate_dash(tag="test_tag_422", title="Test"))
    print(test.create_dash())


    # Delete dash based on uid if left blank as initialized in object
    # print(test.delete_dash(uid='HoR8TpWVk'))

    # Testing anotation push
    utc_end = int(time.time() * 1000)
    utc_start = utc_end + 9000

    print(utc_start)
    anomaly_tags = ['tagged_anomaly']
    push_msg = "This is a message used for pushed anomalies"

    # Dash id to be used
    dashinf = test.get_dash(tag="test_tag_6662", working_dash=False)
    duid = dashinf[0]
    durl = dashinf[1]
    did = dashinf[2]

    print(did)
    # test.push_annotation(utc_end, utc_start, anomaly_tags, push_msg, dash_id=did)


    print(test.get_annotations(dash_id=did))
    print(len(test.get_annotations(dash_id=did)))

   # Delete annotations
    test.delete_annotation(test.get_annotations(dash_id=did))
