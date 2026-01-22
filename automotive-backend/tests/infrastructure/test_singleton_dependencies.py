"""
Functional tests demonstrating Singleton Pattern violation in dependencies.

ARCHITECTURAL VIOLATION:
- Single database session shared across all HTTP requests
- Singleton repository instances returned by dependency functions
- No transaction isolation between requests
- Potential data corruption in concurrent scenarios
- Memory leaks (session never closes)

These tests demonstrate BEHAVIORAL problems caused by the singleton pattern.
They should FAIL with the current implementation and PASS after fixing.
"""

import pytest
from unittest.mock import Mock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.entities.vehicle import Vehicle
from src.infrastructure.database.models import Base
from src.infrastructure.repositories.sqlite_vehicle_repository import SqliteVehicleRepository
from src.infrastructure.repositories.sqlite_alert_repository import SqliteAlertRepository
from src.web.dependencies import (
    get_vehicle_repository,
    get_alert_repository,
    get_observer_factory,
)


class TestSingletonDependencyViolation:
    """
    Tests demonstrating the Singleton Pattern violation in dependencies.
    
    EXPECTED BEHAVIOR (after fix):
    - Each call to get_vehicle_repository() should return a NEW instance
    - Each call should use a DIFFERENT database session
    - Sessions should be isolated per request
    - Sessions should be properly closed after use
    """

    def test_get_vehicle_repository_returns_same_instance_violation(self):
        """
        VIOLATION: get_vehicle_repository() returns the SAME instance every time.
        
        PROBLEM:
        - All requests share the same repository instance
        - No isolation between concurrent requests
        - State can leak between requests
        
        EXPECTED (after fix):
        - Each call should return a DIFFERENT instance
        - Each instance should have its own session
        
        THIS TEST SHOULD FAIL with current implementation.
        """
        # Act - Call dependency function multiple times
        repo1 = get_vehicle_repository()
        repo2 = get_vehicle_repository()
        repo3 = get_vehicle_repository()
        
        # Assert - THIS SHOULD FAIL (currently returns same instance)
        # After fix, these should be DIFFERENT instances
        assert repo1 is not repo2, (
            "ARCHITECTURAL VIOLATION: get_vehicle_repository() returns singleton instance. "
            "Each call should return a NEW instance with its own database session. "
            "Current behavior causes: "
            "1. No transaction isolation between requests "
            "2. Potential data corruption in concurrent scenarios "
            "3. Memory leaks (session never closes) "
            "4. Thread safety issues"
        )
        
        assert repo2 is not repo3, (
            "ARCHITECTURAL VIOLATION: Repository instances are shared across requests"
        )
        
        assert repo1 is not repo3, (
            "ARCHITECTURAL VIOLATION: Same repository instance reused"
        )

    def test_get_alert_repository_returns_same_instance_violation(self):
        """
        VIOLATION: get_alert_repository() returns the SAME instance every time.
        
        THIS TEST SHOULD FAIL with current implementation.
        """
        # Act
        repo1 = get_alert_repository()
        repo2 = get_alert_repository()
        repo3 = get_alert_repository()
        
        # Assert - THIS SHOULD FAIL
        assert repo1 is not repo2, (
            "ARCHITECTURAL VIOLATION: get_alert_repository() returns singleton instance. "
            "Each call should return a NEW instance with its own database session."
        )
        
        assert repo2 is not repo3, (
            "ARCHITECTURAL VIOLATION: Alert repository instances are shared"
        )

    def test_get_observer_factory_returns_same_instance_violation(self):
        """
        VIOLATION: get_observer_factory() returns the SAME instance every time.
        
        THIS TEST SHOULD FAIL with current implementation.
        """
        # Act
        factory1 = get_observer_factory()
        factory2 = get_observer_factory()
        factory3 = get_observer_factory()
        
        # Assert - THIS SHOULD FAIL
        assert factory1 is not factory2, (
            "ARCHITECTURAL VIOLATION: get_observer_factory() returns singleton instance. "
            "Each call should return a NEW instance."
        )
        
        assert factory2 is not factory3, (
            "ARCHITECTURAL VIOLATION: Observer factory instances are shared"
        )

    def test_repositories_share_same_database_session_violation(self):
        """
        VIOLATION: All repository instances share the SAME database session.
        
        PROBLEM:
        - Single session for all requests
        - No transaction isolation
        - Cannot rollback per request
        - Thread safety issues
        
        EXPECTED (after fix):
        - Each repository should have its own session
        - Sessions should be request-scoped
        
        THIS TEST SHOULD FAIL with current implementation.
        """
        # Act
        vehicle_repo1 = get_vehicle_repository()
        vehicle_repo2 = get_vehicle_repository()
        alert_repo1 = get_alert_repository()
        alert_repo2 = get_alert_repository()
        
        # Assert - THIS SHOULD FAIL (currently all share same session)
        # After fix, each should have DIFFERENT sessions
        assert vehicle_repo1._db is not vehicle_repo2._db, (
            "ARCHITECTURAL VIOLATION: All repository instances share the same database session. "
            "This causes: "
            "1. No transaction isolation between requests "
            "2. Cannot rollback failed transactions per request "
            "3. Potential data corruption in concurrent scenarios "
            "4. Memory leaks (session never closes) "
            "EXPECTED: Each repository should have its own request-scoped session."
        )
        
        assert alert_repo1._db is not alert_repo2._db, (
            "ARCHITECTURAL VIOLATION: Alert repositories share the same session"
        )
        
        assert vehicle_repo1._db is not alert_repo1._db, (
            "ARCHITECTURAL VIOLATION: Different repository types share the same session"
        )

    def test_concurrent_requests_cause_transaction_isolation_violation(self):
        """
        TEST: Verify that concurrent requests have isolated sessions.
        
        SCENARIO:
        - Request 1 gets a repository
        - Request 2 gets a repository
        - Each should have its own session for transaction isolation
        
        THIS TEST SHOULD PASS with the fix.
        """
        # Act - Simulate two concurrent requests using our dependency functions
        repo_request1 = get_vehicle_repository()
        repo_request2 = get_vehicle_repository()
        
        # Assert - Each request should have its own session
        assert repo_request1._db is not repo_request2._db, (
            "ARCHITECTURAL VIOLATION: Concurrent requests share the same database session. "
            "This breaks transaction isolation. "
            "Request 2 can see Request 1's uncommitted changes. "
            "EXPECTED: Each request should have its own isolated session."
        )

    def test_session_is_never_closed_memory_leak_violation(self):
        """
        VIOLATION: Database session is never closed, causing memory leaks.
        
        PROBLEM:
        - Singleton session created at startup
        - Never closed during application lifetime
        - Connections accumulate
        - Memory leaks
        
        EXPECTED (after fix):
        - Sessions should be closed after each request
        - Use context managers or FastAPI Depends with cleanup
        
        THIS TEST SHOULD FAIL with current implementation.
        """
        # Act - Get repository multiple times (simulating multiple requests)
        repo1 = get_vehicle_repository()
        repo2 = get_vehicle_repository()
        
        # In proper implementation, each request should:
        # 1. Create a new session
        # 2. Use the session
        # 3. Close the session
        
        # Assert - THIS SHOULD FAIL
        # We can't directly test if session is closed, but we can verify
        # that different calls should use different sessions
        assert repo1._db is not repo2._db, (
            "ARCHITECTURAL VIOLATION: Singleton session is never closed. "
            "This causes memory leaks as connections accumulate. "
            "EXPECTED: Use per-request sessions with proper cleanup: "
            "```python\n"
            "def get_db_session():\n"
            "    session = SessionLocal()\n"
            "    try:\n"
            "        yield session\n"
            "    finally:\n"
            "        session.close()\n"
            "```"
        )

    def test_cannot_rollback_per_request_violation(self):
        """
        TEST: Verify that each request can independently rollback.
        
        SCENARIO:
        - Request 1 gets a repository
        - Request 2 gets a repository
        - Each should have its own session that can be independently rolled back
        
        THIS TEST SHOULD PASS with the fix.
        """
        # Act - Simulate two concurrent requests using our dependency functions
        repo_request1 = get_vehicle_repository()
        repo_request2 = get_vehicle_repository()
        
        # Assert - Each request should have its own session
        assert repo_request1._db is not repo_request2._db, (
            "ARCHITECTURAL VIOLATION: Cannot rollback per request. "
            "Shared session means rolling back Request 1 would affect Request 2. "
            "EXPECTED: Each request should have its own session that can be "
            "independently committed or rolled back."
        )

    def test_thread_safety_violation_with_shared_session(self):
        """
        VIOLATION: Shared session is not thread-safe for concurrent requests.
        
        PROBLEM:
        - SQLAlchemy sessions are not thread-safe
        - Multiple threads (requests) using same session
        - Race conditions and data corruption
        
        THIS TEST SHOULD FAIL with current implementation.
        """
        # Act - Simulate multiple concurrent requests
        repo1 = get_vehicle_repository()
        repo2 = get_vehicle_repository()
        repo3 = get_vehicle_repository()
        
        # Assert - THIS SHOULD FAIL
        # Each request (potentially in different threads) should have its own session
        assert repo1._db is not repo2._db, (
            "ARCHITECTURAL VIOLATION: Shared session across threads is not thread-safe. "
            "SQLAlchemy sessions are not thread-safe. "
            "Multiple concurrent requests using the same session can cause: "
            "1. Race conditions "
            "2. Data corruption "
            "3. Unexpected behavior "
            "EXPECTED: Use per-request sessions with FastAPI's Depends() "
            "to ensure thread safety."
        )
        
        assert repo2._db is not repo3._db, (
            "ARCHITECTURAL VIOLATION: Thread safety not guaranteed"
        )

    def test_correct_implementation_should_use_fastapi_depends(self):
        """
        DOCUMENTATION TEST: Shows what the CORRECT implementation should look like.
        
        This test documents the expected behavior after fixing the violation.
        
        CORRECT IMPLEMENTATION:
        ```python
        # dependencies.py
        from fastapi import Depends
        from typing import Generator
        
        def get_db_session() -> Generator[Session, None, None]:
            session = SessionLocal()
            try:
                yield session
            finally:
                session.close()
        
        def get_vehicle_repository(
            db: Session = Depends(get_db_session)
        ) -> SqliteVehicleRepository:
            return SqliteVehicleRepository(db)
        
        def get_alert_repository(
            db: Session = Depends(get_db_session)
        ) -> SqliteAlertRepository:
            return SqliteAlertRepository(db)
        ```
        
        BENEFITS:
        - New session per request
        - Automatic session cleanup
        - Transaction isolation
        - Thread-safe
        - Testable (can inject mocks)
        """
        # This test always passes - it's documentation
        expected_implementation = """
        CORRECT IMPLEMENTATION:
        
        1. Remove singleton instances (_db_session, _vehicle_repository, etc.)
        2. Use FastAPI's Depends() for dependency injection
        3. Create new session per request
        4. Use context manager to ensure cleanup
        5. Each repository gets its own session
        
        EXAMPLE:
        
        def get_db_session() -> Generator[Session, None, None]:
            session = SessionLocal()
            try:
                yield session
            finally:
                session.close()
        
        def get_vehicle_repository(
            db: Session = Depends(get_db_session)
        ) -> SqliteVehicleRepository:
            return SqliteVehicleRepository(db)
        
        # In endpoint:
        @app.post("/vehicles")
        def create_vehicle(
            request: CreateVehicleRequest,
            vehicle_repo: VehicleRepository = Depends(get_vehicle_repository)
        ):
            use_case = RegisterVehicleUseCase(vehicle_repository=vehicle_repo)
            # ...
        """
        
        assert True, expected_implementation


class TestSingletonViolationImpact:
    """
    Tests demonstrating the REAL-WORLD IMPACT of the singleton violation.
    
    These tests show actual bugs that can occur in production.
    """

    def test_data_corruption_scenario_with_concurrent_updates(self):
        """
        TEST: Verify that concurrent updates have isolated sessions.
        
        SCENARIO:
        - Request 1 gets a repository
        - Request 2 gets a repository
        - Each should have its own session to prevent data corruption
        
        THIS TEST SHOULD PASS with the fix.
        """
        # Act - Simulate two concurrent requests using our dependency functions
        repo_request1 = get_vehicle_repository()
        repo_request2 = get_vehicle_repository()
        
        # Assert - Each request should have its own session
        assert repo_request1._db is not repo_request2._db, (
            "ARCHITECTURAL VIOLATION: Concurrent updates use shared session. "
            "This can cause data corruption. "
            "REAL-WORLD IMPACT: "
            "- Request 1 updates mileage to 10000 "
            "- Request 2 updates mileage to 15000 "
            "- Race condition: which update wins? "
            "- Lost updates and data inconsistency "
            "EXPECTED: Each request should have isolated transaction."
        )

    def test_memory_leak_accumulation_over_time(self):
        """
        REAL-WORLD BUG: Memory leaks accumulate as application runs.
        
        SCENARIO:
        - Application receives 1000 requests
        - Each request should create and close a session
        - With singleton, session is never closed
        - Connections accumulate
        - Eventually runs out of database connections
        
        THIS TEST SHOULD FAIL with current implementation.
        """
        # Simulate multiple requests
        repositories = []
        for i in range(10):
            repo = get_vehicle_repository()
            repositories.append(repo)
        
        # Assert - THIS SHOULD FAIL
        # All repositories should have DIFFERENT sessions
        unique_sessions = set(id(repo._db) for repo in repositories)
        
        assert len(unique_sessions) == len(repositories), (
            f"ARCHITECTURAL VIOLATION: Memory leak detected. "
            f"Expected {len(repositories)} unique sessions, got {len(unique_sessions)}. "
            f"REAL-WORLD IMPACT: "
            f"- Database connections never closed "
            f"- Memory usage grows over time "
            f"- Eventually exhausts connection pool "
            f"- Application crashes under load "
            f"EXPECTED: Each request creates and closes its own session."
        )

    def test_transaction_rollback_affects_other_requests(self):
        """
        TEST: Verify that each request has independent transaction control.
        
        SCENARIO:
        - Request 1 gets a repository
        - Request 2 gets a repository
        - Each should have its own session for independent rollback
        
        THIS TEST SHOULD PASS with the fix.
        """
        # Act - Simulate two concurrent requests using our dependency functions
        repo_request1 = get_vehicle_repository()
        repo_request2 = get_vehicle_repository()
        
        # Assert - Each request should have its own session
        assert repo_request1._db is not repo_request2._db, (
            "ARCHITECTURAL VIOLATION: Shared session causes unintended rollbacks. "
            "REAL-WORLD IMPACT: "
            "- Request 1 creates vehicle V-001 "
            "- Request 2 creates vehicle V-002 "
            "- Request 1 fails and calls session.rollback() "
            "- Request 2's vehicle V-002 is also rolled back! "
            "- Data loss and inconsistent state "
            "EXPECTED: Each request should have isolated transaction that can be "
            "independently committed or rolled back."
        )
