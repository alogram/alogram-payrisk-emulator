# coding: utf-8
import logging
import time
from typing import Optional, Dict, Any, List

from payrisk_base_server.apis.risk_scoring_api_base import BaseRiskScoringApi
from payrisk_base_server.apis.signal_intelligence_api_base import BaseSignalIntelligenceApi
from payrisk_base_server.apis.forensic_data_api_base import BaseForensicDataApi
from payrisk_base_server.apis.roadmap_preview_api_base import BaseRoadmapPreviewApi
from payrisk_base_server.apis.system_api_base import BaseSystemApi

from payrisk_base_server.models.check_request import CheckRequest
from payrisk_base_server.models.decision_response import DecisionResponse
from payrisk_base_server.models.fraud_score import FraudScore
from payrisk_base_server.models.scores_success_response import ScoresSuccessResponse
from payrisk_base_server.models.risk_breakdown import RiskBreakdown
from payrisk_base_server.models.category_signal import CategorySignal
from payrisk_base_server.models.risk_level_enum import RiskLevelEnum
from payrisk_base_server.models.payment_event import PaymentEvent
from payrisk_base_server.models.signals_request import SignalsRequest
from payrisk_base_server.models.account_check_request import AccountCheckRequest
from payrisk_base_server.models.kyc_check_request import KycCheckRequest

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("alogram.payrisk.emulator")


class PayriskApiImpl(
    BaseRiskScoringApi, 
    BaseSignalIntelligenceApi, 
    BaseForensicDataApi, 
    BaseRoadmapPreviewApi, 
    BaseSystemApi
):
    async def risk_check(
        self,
        x_idempotency_key: str,
        check_request: CheckRequest,
        x_trace_id: Optional[str] = None,
    ) -> DecisionResponse:
        logger.info(
            f"🔍 RECEIVED RISK CHECK | IdempotencyKey: {x_idempotency_key} | TraceId: {x_trace_id}"
        )

        # 📱 Phone Intelligence Simulation
        identity = getattr(check_request, "identity", None)
        phone = getattr(identity, "phone", None) if identity else None
        
        identity_signal = CategorySignal(level=RiskLevelEnum.LOW, score=0.01)
        
        if phone:
            logger.info(f"📱 Processing Phone Intelligence for: ***{str(phone)[-4:]}")
            # Simulate different forensics based on phone number suffix
            if phone.endswith("666"):  # 🚨 High Risk / Spam
                identity_signal = CategorySignal(
                    level=RiskLevelEnum.HIGH, 
                    score=0.85, 
                    reasons=["PHONE_SPAM_REGISTRY_MATCH"],
                )
            elif phone.endswith("999"):  # ⚠️ Synergy Risk (VOIP + Spam)
                identity_signal = CategorySignal(
                    level=RiskLevelEnum.HIGH,
                    score=0.99, 
                    reasons=["PHONE_FORENSIC_SYNERGY_CRITICAL"]
                )
            else:  # ✅ Clean Number
                identity_signal = CategorySignal(level=RiskLevelEnum.LOW, score=0.0)

        # Return a standard "approve" decision for the emulator
        decision = DecisionResponse(
            assessment_id=f"ast_{x_idempotency_key.split('_')[-1]}",
            decision="approve" if identity_signal.score < 0.9 else "decline",
            risk_score=identity_signal.score or 0.01,
            decision_score=identity_signal.score or 0.01,
            fraud_score=FraudScore(
                score=identity_signal.score or 0.01, 
                risk_level=identity_signal.level,
                explanation="Spec-compliant emulator assessment"
            ),
            decision_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            breakdown=RiskBreakdown(identity=identity_signal),
            payment_intent_id=f"pi_{hash(x_idempotency_key) % 10**32:032x}",
            ttl_seconds=3600,
            actions=[],
            reason_codes=[]
        )

        logger.info(
            f"✅ EMITTED DECISION | IdempotencyKey: {x_idempotency_key} | Decision: {decision.decision} | Risk: {decision.decision_score}"
        )
        return decision

    async def ingest_payment_event(
        self, x_idempotency_key, payment_event, x_trace_id
    ) -> None:
        logger.info(
            f"📥 INGESTED EVENT | IdempotencyKey: {x_idempotency_key} | Type: {payment_event.event_type}"
        )
        return None

    async def ingest_signals(
        self, x_idempotency_key, signals_request, x_trace_id
    ) -> None:
        count = 0
        if signals_request and signals_request.actual_instance:
            count = len(getattr(signals_request.actual_instance, "signals", []))
        
        logger.info(
            f"📡 INGESTED SIGNALS | IdempotencyKey: {x_idempotency_key} | Count: {count}"
        )
        return None

    async def get_fraud_scores(
        self,
        tenantId,
        x_trace_id=None,
        x_idempotency_key=None,
        start_time=None,
        end_time=None,
        page_size=50,
        page_token=None,
    ) -> ScoresSuccessResponse:
        logger.info(f"📊 FETCHED FRAUD SCORES | Tenant: {tenantId}")
        return ScoresSuccessResponse(scores=[])

    async def health_check(self) -> None:
        return None

    async def account_risk_check(
        self, x_idempotency_key, account_check_request, x_trace_id
    ) -> DecisionResponse:
        logger.info(f"👤 ACCOUNT RISK CHECK | IdempotencyKey: {x_idempotency_key}")
        # Re-use risk_check logic with a dummy CheckRequest
        dummy_req = CheckRequest(entities=None, purchase=None)
        return await self.risk_check(x_idempotency_key, dummy_req, x_trace_id)

    async def kyc_risk_check(
        self, x_idempotency_key, kyc_check_request, x_trace_id
    ) -> DecisionResponse:
        logger.info(f"🆔 KYC RISK CHECK | IdempotencyKey: {x_idempotency_key}")
        dummy_req = CheckRequest(entities=None, purchase=None)
        return await self.risk_check(x_idempotency_key, dummy_req, x_trace_id)
