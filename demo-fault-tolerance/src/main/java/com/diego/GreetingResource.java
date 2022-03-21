package com.diego;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

import java.nio.charset.Charset;
import java.net.MalformedURLException;
import java.net.URL;
import java.io.IOException;

import org.apache.commons.io.IOUtils;
import org.eclipse.microprofile.faulttolerance.Bulkhead;
import org.eclipse.microprofile.faulttolerance.Fallback;
import org.eclipse.microprofile.faulttolerance.Retry;
import org.eclipse.microprofile.faulttolerance.Timeout;
import org.json.JSONException;
import org.json.JSONObject;

@Path("/youtube")
public class GreetingResource {

    private String KEY = "AIzaSyB-l9Dhu0twbJcpT5XKbCku9VTpaf044Ck";

    @GET
    @Timeout(value = 50000L)
    @Retry(maxRetries = 5)
    @Bulkhead(value = 5)
    @Fallback(fallbackMethod = "YT_data_fallback")
    @Produces(MediaType.TEXT_PLAIN)
    public String YT_data() throws IOException, InterruptedException { 
        String ID = "PLF1JyjLWjPnSifcQO7CQx8u3255yHxOsh";
        String url = "https://www.googleapis.com/youtube/v3/playlistItems?playlistId="+ID+"&key=" +KEY+"&part=contentDetails";
        JSONObject json = new JSONObject(IOUtils.toString(new URL(url), Charset.forName("UTF-8")));
        return json.toString(4); 
    }

    public String YT_data_fallback() throws JSONException, MalformedURLException, IOException{
        String ID = "PLRW7iEDD9RDQjStVF3FjOUlTmhR2d0_tU";
        String url = "https://www.googleapis.com/youtube/v3/playlistItems?playlistId="+ID+"&key=" +KEY+"&part=contentDetails&maxResults=50";

        JSONObject json = new JSONObject(IOUtils.toString(new URL(url), Charset.forName("UTF-8")));
        return json.toString(4);
    }
}