from typing import Optional

from services.star.routes import router as star_router
from services.tact.routes import router as tact_router
from services.yeep.routes import router as yeep_router
from services.yeet.routes import router as yeet_router

from utils.server import serve

serve.include_router(star_router)
serve.include_router(tact_router)
serve.include_router(yeep_router)
serve.include_router(yeet_router)
