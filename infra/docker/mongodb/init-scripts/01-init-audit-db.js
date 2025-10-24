// =============================================================================
// MONGODB INITIALIZATION SCRIPT
// Create HR Lookout Audit database and collections
// =============================================================================

// Switch to audit database
db = db.getSiblingDB('hr_lookout_audit');

// Create collections with validation schemas
db.createCollection('audit_logs', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['timestamp', 'service', 'action', 'user_id', 'resource_type'],
      properties: {
        timestamp: {
          bsonType: 'date',
          description: 'Timestamp of the audit event'
        },
        service: {
          bsonType: 'string',
          description: 'Microservice that generated the event'
        },
        action: {
          enum: ['CREATE', 'READ', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT', 'EXPORT'],
          description: 'Action performed'
        },
        user_id: {
          bsonType: 'string',
          description: 'ID of the user who performed the action'
        },
        user_email: {
          bsonType: 'string',
          description: 'Email of the user'
        },
        resource_type: {
          bsonType: 'string',
          description: 'Type of resource affected (e.g., Employee, Payslip)'
        },
        resource_id: {
          bsonType: 'string',
          description: 'ID of the affected resource'
        },
        ip_address: {
          bsonType: 'string',
          description: 'IP address of the request'
        },
        user_agent: {
          bsonType: 'string',
          description: 'User agent string'
        },
        changes: {
          bsonType: 'object',
          description: 'Details of changes made (before/after)'
        },
        metadata: {
          bsonType: 'object',
          description: 'Additional contextual information'
        }
      }
    }
  }
});

// Create indexes for audit_logs
db.audit_logs.createIndex({ timestamp: -1 });
db.audit_logs.createIndex({ service: 1, timestamp: -1 });
db.audit_logs.createIndex({ user_id: 1, timestamp: -1 });
db.audit_logs.createIndex({ resource_type: 1, resource_id: 1 });
db.audit_logs.createIndex({ action: 1, timestamp: -1 });

// Create collection for application error logs
db.createCollection('error_logs', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['timestamp', 'service', 'level', 'message'],
      properties: {
        timestamp: {
          bsonType: 'date',
          description: 'Timestamp of the error'
        },
        service: {
          bsonType: 'string',
          description: 'Microservice that generated the error'
        },
        level: {
          enum: ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
          description: 'Log level'
        },
        message: {
          bsonType: 'string',
          description: 'Error message'
        },
        stack_trace: {
          bsonType: 'string',
          description: 'Stack trace if available'
        },
        user_id: {
          bsonType: 'string',
          description: 'User ID if applicable'
        },
        request_id: {
          bsonType: 'string',
          description: 'Request ID for tracing'
        },
        metadata: {
          bsonType: 'object',
          description: 'Additional contextual information'
        }
      }
    }
  }
});

// Create indexes for error_logs
db.error_logs.createIndex({ timestamp: -1 });
db.error_logs.createIndex({ service: 1, level: 1, timestamp: -1 });
db.error_logs.createIndex({ level: 1, timestamp: -1 });

// Create collection for system events
db.createCollection('system_events', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['timestamp', 'event_type', 'service'],
      properties: {
        timestamp: {
          bsonType: 'date',
          description: 'Timestamp of the event'
        },
        event_type: {
          bsonType: 'string',
          description: 'Type of system event'
        },
        service: {
          bsonType: 'string',
          description: 'Service that generated the event'
        },
        severity: {
          enum: ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
          description: 'Event severity'
        },
        description: {
          bsonType: 'string',
          description: 'Event description'
        },
        metadata: {
          bsonType: 'object',
          description: 'Additional event data'
        }
      }
    }
  }
});

// Create indexes for system_events
db.system_events.createIndex({ timestamp: -1 });
db.system_events.createIndex({ event_type: 1, timestamp: -1 });
db.system_events.createIndex({ severity: 1, timestamp: -1 });

// Create read-only user for analytics (optional)
db.createUser({
  user: 'audit_reader',
  pwd: 'audit_reader_password_2025',
  roles: [
    { role: 'read', db: 'hr_lookout_audit' }
  ]
});

print('MongoDB audit database initialized successfully');
print('Collections created: audit_logs, error_logs, system_events');
