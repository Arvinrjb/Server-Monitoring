# Overview

## Overview
This monitoring system is designed to track server performance and health metrics. It follows a Push-based architecture, where client-side agents report data to a central API server for processing, storage, and alerting.

## System Components
- Agent: A lightweight script installed on target servers that collects metrics (CPU, RAM, Disk, etc.) and system logs, then pushes them to the backend API.
- Backend API (Django): The core service that handles incoming data, performs validation, and orchestrates status updates.
- Alert Engine: Monitors incoming data for thresholds (>90%) and generates alert records in the database.
